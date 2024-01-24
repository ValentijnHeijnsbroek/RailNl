import random
import copy
import pandas as pd
from help_funtions import initialize_rail, greedy_decision

# Load the connection data
file_path = '../data/ConnectiesHolland.csv'
connection_data = pd.read_csv(file_path)

# Constants
max_aantal_minuten = 160
max_aantal_trajecten = 20
threshold_visit_frequency = 3  # Adjust as needed

# Function to find central hubs
def find_central_hubs(connection_data):
    connection_counts = (connection_data['station1'].value_counts() + connection_data['station2'].value_counts()).fillna(0)
    central_hubs = connection_counts.sort_values(ascending=False).index.tolist()
    return central_hubs

central_hubs = find_central_hubs(connection_data)

def can_add_station(traject, station, visited_stations, station_visit_frequency):
    if len(traject.traject_stations) >= 10:
        return False
    if station_visit_frequency.get(station.name, 0) > threshold_visit_frequency:
        return False
    return True

def depth_first_search(rail, traject, traject_index, visited_stations, uncovered_stations, current_depth, max_depth, current_score, central_hubs):
    station_visit_frequency = {}

    if current_depth >= max_depth:
        return False

    score_improved = False

    next_station = greedy_decision(rail, traject_index)

    if next_station and can_add_station(traject, next_station, visited_stations, station_visit_frequency):
        traject.add_station_to_traject(next_station)
        visited_stations.add(next_station)
        station_visit_frequency[next_station.name] = station_visit_frequency.get(next_station.name, 0) + 1

        if rail.sum_time(traject_index) <= max_aantal_minuten:
            new_score = rail.get_score()
            # Ensure traject has more than one station before updating the score
            if (new_score > current_score or len(traject.traject_stations) < 2) and len(traject.traject_stations) > 1:
                score_improved = True
                if depth_first_search(rail, traject, traject_index, visited_stations, uncovered_stations, current_depth + 1, max_depth, new_score, central_hubs):
                    return True

        visited_stations.remove(next_station)
        traject.delete_latest_station()

    return score_improved


def iterative_depth_first(max_depth, iterations, central_hubs):
    best_rail = None
    best_score = 0

    for iteration in range(iterations):
        print(f"Progress: {iteration / iterations * 100:.2f}%")
        current_rail = initialize_rail('Holland')
        valid_traject_count = 0
        new_score = 0

        for traject_index in range(1, max_aantal_trajecten + 1):
            new_traject = current_rail.create_traject(traject_index)
            
            # Prefer central hubs as start stations
            if central_hubs:
                start_station_name = central_hubs.pop(0)
                start_station = next((s for s in current_rail.stations if s.name == start_station_name), None)
            else:
                start_station = random.choice(current_rail.stations)

            new_traject.add_station_to_traject(start_station)
            visited_stations = set([start_station])

            traject_improved = depth_first_search(current_rail, new_traject, traject_index, visited_stations, set(current_rail.stations), 0, max_depth, 0, central_hubs)

            if len(new_traject.traject_stations) > 1:
                valid_traject_count += 1
                new_score = current_rail.get_score()
                if new_score > best_score:
                    best_score = new_score
                    best_rail = copy.deepcopy(current_rail)

            if valid_traject_count >= max_aantal_trajecten or new_score == best_score:
                break

        print(f"End of iteration {iteration + 1}, Best score: {best_score}")

    if best_rail:
        best_rail.print_output()
    else:
        print("No optimal rail configuration found.")
    return best_rail

# Example usage
max_depth = 20
iterations = 50000
best_rail = iterative_depth_first(max_depth, iterations, central_hubs)
