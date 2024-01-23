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
    
    def get_score(self, rail_network):
        duration_traject = 0
        T = 1
        for i in range(len(self.traject) - 1):
            station_1 = self.traject[i]
            station_2 = self.traject[i+1]
            if station_1.connections_durations[station_2]:
                duration_traject += station_1.connections_durations[station_2]
        
        p = len(self.traject) / rail_network.amount_of_connections  # the fraction of the traveled connections (between 0 and 1)
        K = p * 10000 - (T * 100 + duration_traject) 
        return round(K, 2)
        
        
    
class ACO():
    def __init__(self):
        self.pheromones = {}
        self.ants = []
        self.current_station = None
        self.totaal_trajecten = {}

        
        
    def set_pheromones(self, connection_filename):
        with open(connection_filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                station_1 = row[0]
                station_2 = row[1]
                self.pheromones[(station_1, station_2)] = 1
        print("pheromones set", self.pheromones)
        
    def deploy_ants(self, rail_network, num_ants):
        for i in range(num_ants):
            ant = Ant(rail_network.stations[randint(0, len(rail_network.stations) - 1)])
            self.ants.append(ant)
        return self.ants

    def get_connections(self, station):
        search_result = {key[0] if key[1] == station else key[1]: value for key, value in self.pheromones.items() if station in key}
        return search_result
        
    
    def choose_next_station(self, ant, pheromones, max_stations):
        # Get all possible connections from the current station
        possible_connections = [connection for connection in ant.current_station.connections if not ant.is_bereden(connection)]
        if len(ant.traject) >= max_stations:
            return None
        
        if possible_connections:
            
            names_connections = [connection.name for connection in possible_connections]
            
            
            find_pheromones = self.get_connections(ant.current_station.name)
            
            
            # Calculate the total pheromone level for all possible connections
            
            total_pheromone = sum(find_pheromones.values())
            
            # Calculate the probabilities for each possible connection based on pheromone levels
            probabilities = [find_pheromones[connection.name] / total_pheromone for connection in possible_connections]
            print("Probabilities:", probabilities)
            # Choose the next connection based on the probabilities
            print("Possible connections:", possible_connections)
            next_connection = choices(possible_connections, weights = probabilities)[0]
            print("Next connection:", next_connection)
            
            return next_connection
        
            
        else:
            print("No connections")
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
        print("Best solution:", best_solution)  
        for connection in best_solution:
            for i in range(len(best_solution) - 1):
                station_1 = best_solution[i]
                station_2 = best_solution[i+1]
                if station_1.connections_durations[station_2]:
                    try:
                        self.pheromones[(station_1.name, station_2.name)] += 1 / best_score
                    except KeyError:
                        self.pheromones[(station_2.name, station_1.name)] += 1 / best_score
                    print("pheromones:", self.pheromones)
                    
# Initialize parameters
num_ants = 10
num_iterations = 10
evaporation_rate = 0.1

#main loop
if __name__ == "__main__":
    rail_network = RailNL()
    aco = ACO()
    rail_network.load_stations('StationsHolland.csv')
    rail_network.load_connections('ConnectiesHolland.csv')
    aco.set_pheromones('ConnectiesHolland.csv')

    for i in range(num_iterations):
        ants = aco.deploy_ants(rail_network, num_ants)
        
        for ant in ants:
            while ant.current_station is not None:
                ant.current_station = aco.choose_next_station(ant, aco.pheromones, 7)
                if ant.current_station is not None:
                    ant.traject.append(ant.current_station)
            
            aco.update_pheromones(rail_network, evaporation_rate)
            
        # Print information after each iteration
        print("Iteration:", i + 1)
        for ant in ants:
            print("Score:", ant.get_score(rail_network))
            print("Trajectory:", ant.traject)
            print("Pheromones:", aco.pheromones)
            aco.totaal_trajecten[ant] = ant.traject
        print("Totaal trajecten:", aco.totaal_trajecten)
        score_totaal = rail_network.get_score()
        print("Score totaal:", score_totaal)    
        print("------")
        






