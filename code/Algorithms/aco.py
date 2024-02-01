import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from random import *
from Classes.railnl import RailNL
import csv
from Classes.railnl import Station


from random import randint, choices, choice
from typing import List, Dict, Union, Tuple

class Ant:
    def __init__(self, begin_station: 'Station'):
        self.begin_station = begin_station
        self.current_station = self.begin_station
        self.traject: List['Station'] = []
        self.traject.append(self.current_station)
        

    def is_visited(self, station: 'Station') -> bool:
        """
        Returns True if the ant has already visited the station, False otherwise.
        
        Pre: station is a station in the rail network.
        Post: True is returned if the ant has already visited the station, False otherwise.
        """	
        return station in self.traject

   
    def get_duration(self) -> int:
        """
        Returns the duration of the trajectory of the ant.

        Post: The duration of the traject of the ant is returned.
        """	
        duration_traject = 0
        for i in range(len(self.traject) - 1):
            station_1 = self.traject[i]
            station_2 = self.traject[i + 1]
            if station_1.connections_durations[station_2]:
                duration_traject += station_1.connections_durations[station_2]
        return duration_traject

    
    def get_score(self, rail_network: 'RailNL') -> float:
        """
        Returns the score of the traject of an individual ant using the provided score-function.

        Pre: rail_network is a rail network.
        Post: The score of the traject of an individual ant is returned.
        """	
        T = 1
        p = len(self.traject) / rail_network.amount_of_connections
        K = p * 10000 - (T * 100 + self.get_duration())
        return round(K, 2)


class ACO:
    def __init__(self):
        self.pheromones: Dict[Tuple[str, str], float] = {}
        self.ants: List[Ant] = []
        self.current_station: Union[None, 'Station'] = None
        self.totaal_trajecten: Dict[Ant, List['Station']] = {}
        self.unique_connections: set[Tuple[str, str]] = set()
        self.duration_totaal: int = 0

    
    def set_pheromones(self, connection_filename: str) -> None:
        """
        Initializes the pheromones dictionary of the connections in the rail network.

        Pre: connection_filename is the name of a file containing the connections of the rail network.
        Post: The pheromones dictionary of the connections in the rail network is initialized.
        """
        with open(connection_filename, 'r') as file:
            # Assuming CSV format, adjust if using a different format
            # Assuming 'Station' class has a 'name' attribute
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                station_1 = row[0]
                station_2 = row[1]
                self.pheromones[(station_1, station_2)] = 1

    
    def deploy_ants(self, rail_network: 'RailNL', num_ants: int) -> List[Ant]:
        """
        Deploys a specified number of ants on the rail network.

        Pre: rail_network is a rail network, num_ants is an integer.
        Post: A list of ants is returned.
        """	
        self.ants = [Ant(choice(rail_network.stations)) for _ in range(num_ants)]
        return self.ants

    
    def get_connections(self, station: str) -> Dict[str, float]:
        """
        Extracts the connections of a station from the pheromones dictionary.

        Pre: station is the name of a station in the rail network.
        Post: A dictionary containing the connections of the station and their pheromone values is returned.
        """
        search_result = {key[0] if key[1] == station else key[1]: value for key, value in self.pheromones.items() if station in key}
        return search_result

    
    def choose_next_station(self, ant: Ant, max_duration: int, exploration_parameter: float) -> Union['Station', None]:
        """
        Determines the next station for an ant to visit by looking into the possible connections. 
        Then a weighted random decision is made based on the level of the exploration_parameter and 
        the pheromone levels of the possible connections.

        Pre: ant is an ant, max_duration is an integer, exploration_parameter is a float.
        Post: The next station for the ant to visit is returned, if no station available or found it returns None.
        """
        possible_connections = [connection for connection in ant.current_station.connections if not ant.is_visited(connection)]
        filtered_connections = [station for station in possible_connections if ant.get_duration() + station.connections_durations[ant.current_station] <= max_duration]

        if filtered_connections:
            find_pheromones = self.get_connections(ant.current_station.name)
            filtered_pheromones = {key: value for key, value in find_pheromones.items() if key in [connection.name for connection in filtered_connections]}
            total_pheromone = sum(filtered_pheromones.values())

            pheromone_probabilities = [find_pheromones[connection.name] / total_pheromone for connection in filtered_connections]
            exploration_prob = 1 - exploration_parameter
            exploration_weights = [exploration_prob / len(filtered_connections) for _ in filtered_connections]

            probabilities = [exploration_prob * p + exploration_parameter * r_prob for p, r_prob in zip(pheromone_probabilities, exploration_weights)]
            next_connection = choices(filtered_connections, weights=probabilities)[0]
            return next_connection
        else:
            return None

    
    def update_pheromones(self, rail_network: 'RailNL', evaporation_rate: float) -> None:
        """
        Updates the pheromones of the connections in the rail network. All pheromones are evaporated 
        and the pheromones of the connections of the best solution are updated.

        Pre: rail_network is a rail network, evaporation_rate is a float.
        Post: The pheromones of the connections in the rail network are updated.
        """	
        best_solution = None
        best_score = 0
        for ant in self.ants:
            if ant.get_score(rail_network) > best_score:
                best_score = ant.get_score(rail_network)
                best_solution = ant.traject

        for connection in self.pheromones:
            self.pheromones[connection] *= (1 - evaporation_rate)

        for connection in best_solution:
            for i in range(len(best_solution) - 1):
                station_1 = best_solution[i]
                station_2 = best_solution[i + 1]
                if station_1.connections_durations[station_2]:
                    try:
                        self.pheromones[(station_1.name, station_2.name)] += 1 / best_score
                    except KeyError:
                        self.pheromones[(station_2.name, station_1.name)] += 1 / best_score

    
    def total_score(self, rail_network) -> float:
        """
        Returns the total score of the rail network according to the provided score-function.

        Pre: rail_network is a rail network.
        Post: The total score of the rail network according to the provided score-function is returned.
        """	
        self.duration_totaal = 0
        self.unique_connections.clear()
        for ant in self.ants:
            duration_traject = 0
            for i in range(len(ant.traject) - 1):
                station_1 = ant.traject[i]
                station_2 = ant.traject[i + 1]
                connection = (station_1.name, station_2.name)
                self.update_unique_connections(connection)
                if station_1.connections_durations[station_2]:
                    duration_traject += station_1.connections_durations[station_2]

            self.duration_totaal += duration_traject

        p = len(self.unique_connections) / rail_network.amount_of_connections
        k = p * 10000 - (len(self.ants) * 100 + self.duration_totaal)
        return round(k, 2)

    
    def update_unique_connections(self, connection: Tuple[str, str]) -> None:
        """
        Updates the set of unique connections in the rail network. 
        This is used to calculate the score of the rail network.

        Pre: connection is a tuple containing the names of two stations in the rail network.
        Post: The set of unique connections in the rail network is updated.
        """	
        self.unique_connections.add(tuple(sorted(connection)))


# Initialize parameters

num_iterations: int = 500000
evaporation_rate: float = 0.001
max_duration: int = 180
exploration_parameter: float = 0.5
min_trajecten: int = 3
max_trajecten: int = 18
end_random_iterations: int = 10000
calculations_done: bool = False
threshold: int = 700000
network_size_stations = 'StationsNationaal.csv'
network_size_connections = 'ConnectiesNationaal.csv'
# main loop
if __name__ == "__main__":
    rail_network = RailNL()
    aco = ACO()
    rail_network.load_stations(network_size_stations)
    rail_network.load_connections(network_size_connections)
    aco.set_pheromones(network_size_connections)
    best_score: float = 0
    best_netwerk: Union[None, Dict[Ant, List['Station']]] = None
    best_duration: int = 0
    list_scores: List[float] = []
    best_scores_num_traject: dict = {}
    best_score_not_changed: int = 0
    for i in range(1, 21):
        best_scores_num_traject[i] = 0
    

    for i in range(num_iterations):
        # num_ants = randint(min_trajecten, max_trajecten)
        if i < end_random_iterations:
            # num_ants = 20 - round(i / (num_iterations / 20))
            num_ants = randint(min_trajecten, max_trajecten)
        else:
            if not calculations_done:
                sum_scores = sum(best_scores_num_traject.values())
                weights = [score / sum_scores for score in best_scores_num_traject.values()]
                calculations_done = True
            num_ants = choices(list(best_scores_num_traject.keys()), weights=weights)[0]    
        ants = aco.deploy_ants(rail_network, num_ants)
        aco.totaal_trajecten.clear()

        for ant in ants:
            while ant.current_station is not None:
                ant.current_station = aco.choose_next_station(ant, max_duration, exploration_parameter)
                if ant.current_station is not None:
                    ant.traject.append(ant.current_station)
                    aco.update_unique_connections((ant.traject[-2].name, ant.traject[-1].name))

            aco.update_pheromones(rail_network, evaporation_rate)
            aco.totaal_trajecten[ant] = ant.traject
            # print(ant.get_duration())
        exploration_parameter = max(0.1, exploration_parameter * 0.9999)
        list_scores.append(aco.total_score(rail_network))
        
          # to save data in a txt file to compare in a histogram
        with open('../data/scores/aco_scores.txt', 'w') as f:
                for score in list_scores:
                    f.write(f"{score}\n")

        avg_score = sum(list_scores) / len(list_scores)
        if i % 10 == 0:
            print(f"{round(i / num_iterations * 100, 2)} %", avg_score, best_score, best_score_not_changed)

        for ant, trajectory in aco.totaal_trajecten.items():
            station_names = [station.name for station in trajectory]

        score_totaal = aco.total_score(rail_network)
        if score_totaal > best_score:
            prev_best_score = best_score
            best_score = score_totaal
            best_netwerk = aco.totaal_trajecten
            best_duration = aco.duration_totaal
            best_iteration = i + 1
            best_score_not_changed = 0
        elif i > end_random_iterations:
            best_score_not_changed += 1
        if best_score_not_changed > threshold or best_score - prev_best_score < 10:
            print(f"Best score not changed for {threshold} iterations {best_score_not_changed}")
            break
         
        if score_totaal > best_scores_num_traject[len(aco.totaal_trajecten)]:
            best_scores_num_traject[len(aco.totaal_trajecten)] = score_totaal
            
        
    print("Best score:", best_score)
    print("Best iteration:", best_iteration)

    for trajectory in best_netwerk.values():
        station_names = [station.name for station in trajectory]
        print(station_names)
    
