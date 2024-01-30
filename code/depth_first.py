import random
import copy
import pandas as pd
from help_funtions import initialize_rail
from railnl import RailNL
import matplotlib.pyplot as plt
from station import Station
from traject import Traject
from typing import List, Set

# Load the connection data
file_path: str = '../data/ConnectiesNationaal.csv'
connection_data: pd.DataFrame = pd.read_csv(file_path)

# Constants
max_aantal_minuten: int = 180
max_aantal_trajecten: int = 15
threshold_visit_frequency: int = 9  # Adjust as needed
MAX_ATTEMPTS: int = 400
min_stations: int = 3

# Function to find central hubs
def find_central_hubs(connection_data: pd.DataFrame) -> List[str]:
    """
    Makes a list of the stations with the most connections to the least connection

    pre: connection data of each station
    post: central hubs list
    """
    connection_counts: pd.Series = (connection_data['station1'].value_counts() + connection_data['station2'].value_counts()).fillna(0)
    central_hubs: List[str] = connection_counts.sort_values(ascending=False).index.tolist()
    return central_hubs

# make the list global
central_hubs: List[str] = find_central_hubs(connection_data)

def can_add_station(traject: RailNL, station: Station, visited_stations: Set[Station], station_visit_frequency: dict[Station: int]) -> bool:
    """
    Checks whether the station can be added to the traject or not

    pre: traject object, station object and a variable that checks how many times the station has
        been in the rail
    post: True or False
    """
    if len(traject.traject_stations) > 0:
        last_station: Station = traject.traject_stations[-1]
        if last_station.name == station.name:
            return False

    if len(traject.traject_stations) > 0:
        last_station: Station = traject.traject_stations[-1]
        if not ((connection_data['station1'] == last_station.name) & (connection_data['station2'] == station.name)).any() and \
           not ((connection_data['station2'] == last_station.name) & (connection_data['station1'] == station.name)).any():
            return False
    if len(traject.traject_stations) >= 20:
        return False
    if station_visit_frequency.get(station.name, 0) > threshold_visit_frequency:
        return False
    return True

def update_uncovered_connections(uncovered_connections: Set[tuple], traject: Traject) -> None:
    """
    When a connection has been made it has been covered and then that connection has to
    be removed from the uncovered list

    pre: uncovered connection set, and traject object
    post: updated uncovered connection list for the rail
    """
    if len(traject.traject_stations) >= 2:
        # Get the last two stations in the traject
        last_station: Station = traject.traject_stations[-2]
        new_station: Station = traject.traject_stations[-1]

        # Create connection tuple
        connection: tuple = (last_station.name, new_station.name)

        # Remove the connection from uncovered connections
        if connection in uncovered_connections:
            uncovered_connections.remove(connection)
        # Check and remove the reverse connection as well
        reverse_connection: tuple = (new_station.name, last_station.name)
        if reverse_connection in uncovered_connections:
            uncovered_connections.remove(reverse_connection)

def depth_first_search(rail: RailNL, traject: Traject, traject_index: int, visited_stations: Set[Station],
                      uncovered_connections: Set[tuple], current_depth: int, max_depth: int, current_score: float,
                      central_hubs: List[str]) -> bool:
    """
    Performs a depth-first search to add stations to a rail trajectory.
    This function recursively explores potential stations to add,
    aiming to improve the overall score of the rail network.

    pre: rail object, traject object, traject index,
         visited_stations set, uncovered connection set, current depth int
         max depth int, current score float, and a central hub list.
    post: returns True if adding a station improves the score and meets constraints, otherwise False.
          updates the trajectory and uncovered connections as stations are added.
    """
    if current_depth >= max_depth:
        return False
    station_visit_frequency: dict = {}
    score_improved: bool = False
    best_new_score: float = current_score
    best_new_station: Station = None

    # Explore potential next stations
    for next_station in rail.stations:
        if next_station not in visited_stations and can_add_station(traject, next_station, visited_stations, station_visit_frequency):
            traject.add_station_to_traject(next_station)
            visited_stations.add(next_station)
            update_uncovered_connections(uncovered_connections, traject)

            new_score: float = rail.get_score()

            # Check for score improvement and adherence to time constraints
            if new_score > best_new_score and rail.sum_time(traject_index) <= max_aantal_minuten:
                best_new_score = new_score
                best_new_station = next_station

                # Recursive search with updated score and depth
                if depth_first_search(rail, traject, traject_index, visited_stations, uncovered_connections, current_depth + 1, max_depth, new_score, central_hubs):
                    return True

            # Revert changes for the next iteration
            visited_stations.remove(next_station)
            traject.delete_latest_station()
    if len(traject.traject_stations) < min_stations:
        for i in range(len(traject.traject_stations)):
            traject.delete_latest_station()
        return False
    # Check if a better station was found
    if best_new_station:
        traject.add_station_to_traject(best_new_station)
        visited_stations.add(best_new_station)
        update_uncovered_connections(uncovered_connections, traject)
        score_improved = True

    return score_improved

# score list for histogram
iteration_scores: List[float] = []

def iterative_depth_first(max_depth: int, iterations: int, central_hubs: List[str], no_improvement_threshold: int = 1000) -> RailNL:
    """
    Conducts an iterative depth-first search to optimize a network of rail trajectories.
    The function iterates over multiple attempts to construct an optimal set of trajectories
    aiming to maximize a scoring function given constraints.

    pre: max depth int, iterations int, central hubs list, and a no improvement threshold
    post: returns the best rail network configuration found after all iterations
          when a better rail network has been found it changes the best rail into that one
          when there is no improvement for a given amount of iterations the central hub list refreshes
          stops trying to make a better rail given a start station after a certain amount of attempts
    """
    best_rail: RailNL = None
    best_score: float = 0
    iterations_without_improvement: int = 0
    uncovered_connections: Set[tuple] = set()
    attempts: int = 0

    for _, row in connection_data.iterrows():
        uncovered_connections.add((row['station1'], row['station2']))
        uncovered_connections.add((row['station2'], row['station1']))

    for iteration in range(iterations):
        if iterations_without_improvement >= no_improvement_threshold:
            central_hubs = find_central_hubs(connection_data)
            iterations_without_improvement = 0

        print(f"Progress: {iteration / iterations * 100:.2f}%")
        current_rail: RailNL = initialize_rail()
        valid_traject_count: int = 0
        new_score: float = 0
        traject_index: int = 0

        while valid_traject_count < max_aantal_trajecten:
            traject_index += 1
            new_traject: Traject = current_rail.create_traject(traject_index)

            if central_hubs:
                start_station_name: str = random.choice(central_hubs)
                central_hubs.remove(start_station_name)
                start_station: Station = next((s for s in current_rail.stations if s.name == start_station_name), None)
            else:
                start_station: Station = random.choice(current_rail.stations)

            new_traject.add_station_to_traject(start_station)
            visited_stations: Set[Station] = set([start_station])

            traject_improved: bool = depth_first_search(current_rail, new_traject, traject_index, visited_stations, uncovered_connections, 0, max_depth, 0, central_hubs)

            if len(new_traject.traject_stations) >= min_stations:
                valid_traject_count += 1
                new_score = current_rail.get_score()

                if new_score > best_score:
                    best_score = new_score
                    best_rail = copy.deepcopy(current_rail)
                    iterations_without_improvement = 0
                else:
                    iterations_without_improvement += 1
            else:
                # If the trajectory is not valid, reduce the traject_index
                traject_index -= 1
            
            with open('../data/depth_first_scores.txt', 'w') as f:
                for score in iteration_scores:
                    f.write(f"{score}\n")

            if attempts > MAX_ATTEMPTS:
                attempts = 0
                break
            attempts += 1
        iteration_scores.append(new_score)
        print(f"End of iteration {iteration + 1}, Best score: {best_score}")

    if best_rail:
        best_rail.print_output()
        best_rail.upload_output('depth_first_search.csv')
    else:
        print("No optimal rail configuration found.")

    plt.hist(iteration_scores, bins=50, color='blue', alpha=0.7)
    plt.xlabel('Scores')
    plt.ylabel('Frequency')
    plt.title('Histogram of Scores')
    plt.grid(True)
    plt.savefig('../data/depthfirst_histogram.png')

    best_rail.plot_network()

    return best_rail

# Example usage
max_depth: int = 75
iterations: int = 240
no_improvement_threshold: int = 40
best_rail: RailNL = iterative_depth_first(max_depth, iterations, central_hubs, no_improvement_threshold)
