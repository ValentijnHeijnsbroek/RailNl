from random import *
from railnl import RailNL
import csv


class Ant():
    def __init__(self, begin_station):
        self.begin_station = begin_station
        self.current_station = self.begin_station
        self.traject = []
        self.traject.append(self.current_station)
      
    
    def add_station(self, station):
        self.traject.append(station)
        self.current_station = station
        
    def is_bereden(self, station):
        return station in self.traject
    
    def get_duration(self):
        duration_traject = 0
        for i in range(len(self.traject) - 1):
            station_1 = self.traject[i]
            station_2 = self.traject[i+1]
            if station_1.connections_durations[station_2]:
                duration_traject += station_1.connections_durations[station_2]
        return duration_traject
    
    def get_score(self, rail_network):
        T = 1
        p = len(self.traject) / rail_network.amount_of_connections  # the fraction of the traveled connections (between 0 and 1)
        K = p * 10000 - (T * 100 + self.get_duration())  # the score of the trajectory (between 0 and 10000)
        return round(K, 2)
        
        
    
class ACO():
    def __init__(self):
        self.pheromones = {}
        self.ants = []
        self.current_station = None
        self.totaal_trajecten = {}
        self.unique_connections = set()
        self.duration_totaal = 0
        
    def set_pheromones(self, connection_filename):
        with open(connection_filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                station_1 = row[0]
                station_2 = row[1]
                self.pheromones[(station_1, station_2)] = 1
        # print("pheromones set", self.pheromones)
        
    def deploy_ants(self, rail_network, num_ants):
        self.ants = [Ant(choice(rail_network.stations)) for _ in range(num_ants)]
        return self.ants

    def get_connections(self, station):
        search_result = {key[0] if key[1] == station else key[1]: value for key, value in self.pheromones.items() if station in key}
        return search_result
        
    
    def choose_next_station(self, ant, max_duration, exploration_parameter):
    # Get all possible connections from the current station
        possible_connections = [connection for connection in ant.current_station.connections if not ant.is_bereden(connection)]
        
        filtered_connections = [station for station in possible_connections if ant.get_duration() + station.connections_durations[ant.current_station] <= max_duration]
            
        if filtered_connections:
            find_pheromones = self.get_connections(ant.current_station.name)
            filtered_pheromones = {key: value for key, value in find_pheromones.items() if key in [connection.name for connection in filtered_connections]} 
            # Calculate the total pheromone level for all possible connections
            total_pheromone = sum(filtered_pheromones.values())
            # Calculate the probabilities for each possible connection based on pheromone levels
            pheromone_probabilities = [find_pheromones[connection.name] / total_pheromone for connection in filtered_connections]
            exploration_prob = 1 - exploration_parameter
            exploration_weights = [exploration_prob / len(filtered_connections) for _ in filtered_connections]
            
            probabilities = [exploration_prob * p + exploration_parameter * r_prob for p, r_prob in zip(pheromone_probabilities, exploration_weights)]
            # Choose the next connection based on the probabilities
            # print("sum probabilities:", sum(probabilities))
            next_connection = choices(filtered_connections, weights=probabilities)[0]
            return next_connection
        else:
            # If no valid next station is found, return None
            return None

        
    def update_pheromones(self, rail_network, evaporation_rate):
        best_solution = None
        best_score = 0
        for ant in self.ants:
            if ant.get_score(rail_network) > best_score:
                best_score = ant.get_score(rail_network)
                best_solution = ant.traject
        # Evaporate pheromones on all connections
        for connection in self.pheromones:
            self.pheromones[connection] *= (1 - evaporation_rate)
        
        # Update pheromones on connections in the best solution
        # print("Best solution:", best_solution)  
        for connection in best_solution:
            for i in range(len(best_solution) - 1):
                station_1 = best_solution[i]
                station_2 = best_solution[i+1]
                if station_1.connections_durations[station_2]:
                    try:
                        self.pheromones[(station_1.name, station_2.name)] += 1 / best_score
                    except KeyError:
                        self.pheromones[(station_2.name, station_1.name)] += 1 / best_score
                    # print("pheromones:", self.pheromones)
                    
    def total_score(self):
        self.duration_totaal = 0
        self.unique_connections.clear()
        for ant in self.ants:
            duration_traject = 0
            for i in range(len(ant.traject) - 1):  # Loop until the second to last element
                station_1 = ant.traject[i]
                station_2 = ant.traject[i+1]
                connection = (station_1.name, station_2.name)
                self.update_unique_connections(connection) 
                if station_1.connections_durations[station_2]:
                    duration_traject += station_1.connections_durations[station_2]      
            self.duration_totaal += duration_traject
            # print("duration_totaal:", duration_totaal)
        # print("Unique connections:", self.unique_connections)   
        # print("length unique connections:", len(self.unique_connections))      
        p = len(self.unique_connections) / rail_network.amount_of_connections
        # print("p:", p)
        k = p * 10000 - (len(self.ants) * 100 + self.duration_totaal)
        # print("duration_totaal:", duration_totaal)  
        return round(k, 2)
        
    
    def update_unique_connections(self, connection):
        self.unique_connections.add(tuple(sorted(connection)))
        
    
            
        
# Initialize parameters

num_iterations = 1000
evaporation_rate = 0.01
max_duration = 180
exploration_parameter = 0.5


#main loop
if __name__ == "__main__":
    rail_network = RailNL()
    aco = ACO()
    rail_network.load_stations('StationsNationaal.csv')
    rail_network.load_connections('ConnectiesNationaal.csv')
    aco.set_pheromones('ConnectiesNationaal.csv')
    best_score = 0
    best_netwerk = None
    list_scores = []
    

    for i in range(num_iterations):
        num_ants = randint(7, 17)
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
        exploration_parameter *= num_iterations/ (num_iterations + 1)
        list_scores.append(aco.total_score())
        avg_score = sum(list_scores) / len(list_scores)
        print(f"{round(i / num_iterations * 100, 2)} %", avg_score)
        
        # Print information after each iteration
        # print("Iteration:", i + 1)
        # print("length totaal trajecten", len(aco.totaal_trajecten))
        
        
        
        # print("Totaal trajecten:")
        for ant, trajectory in aco.totaal_trajecten.items():
            station_names = [station.name for station in trajectory]
             

        
        # print("Totaal trajecten:", aco.totaal_trajecten)
        score_totaal = aco.total_score()
        # print("Score totaal:", score_totaal)
        # print("duration_totaal", aco.duration_totaal)     
        # print("------")
        if score_totaal > best_score:
            best_score = score_totaal
            best_netwerk = aco.totaal_trajecten
            best_duration = aco.duration_totaal
            best_iteration = i + 1
    print("Best score:", best_score)
    print("Best duration:", best_duration)
    print("Best iteration:", best_iteration)
    for trajectory in best_netwerk.values():
        station_names = [station.name for station in trajectory]
        print(station_names)
    # print("pheromones:" , aco.pheromones)
    # print("Best netwerk:", best_netwerk)