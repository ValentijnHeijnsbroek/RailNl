from random import randint, random
from railnl import RailNL
from station import Station
from traject import Traject


class Ant():
    def __init__(self):
        self.begin_station = None
        self.current_station = self.begin_station
        self.traject = []
        self.pheromones = {}
        self.ants = []
    

    def set_pheromones(self, rail_network):
        rail_network.load_stations('StationsHolland.csv')
        rail_network.load_connections('ConnectiesHolland.csv')  
        for connection in rail_network.connections:
            self.pheromones[connection] = 1.0
        
    def deploy_ants(self, rail_network, num_ants):
        for i in range(num_ants):
            self.ants.append(Ant(rail_network.stations[randint(0, len(rail_network.stations) - 1)]))
        return self.ants
    
    def choose_next_station(self, rail_network, pheromones, max_stations):
        list_possible_stations = [station for station in self.current_station.connections if not self.is_bereden(station)]
        if len(self.traject) == max_stations:  
            return None
        
        elif list_possible_stations:
            possible_connections = []
            for station in list_possible_stations:
                possible_connections.append((self.current_station, station))
            
            # Calculate the total pheromone level for all possible connections
            total_pheromone = sum(pheromones[connection] for connection in possible_connections)
            
            # Calculate the probabilities for each possible connection based on pheromone levels
            probabilities = [pheromones[connection] / total_pheromone for connection in possible_connections]
            
            # Choose the next connection based on the probabilities
            next_connection = random.choices(possible_connections, probabilities)[0]
            
            return next_connection[1]
        
            
        else:
            print("No connections")
            return None
        
    def get_score_traject(self, rail_network):
        duration_traject = 0 # Totale duur van het traject
        T = 1 #het aantal  bereden trajecten (standaard 1)
        for connection in range(len(self.traject) - 1):
            duration_traject += rail_network.connections[self.traject[connection], self.traject[connection + 1]]
        
        p =  len(self.traject) / self.amount_of_connections  # de fractie van de bereden verbindingen (dus tussen 0 en 1)
        K = p*10000 - (T*100 + duration_traject) 
        return round(K, 2)
    
    def update_pheromones(self, rail_network, evaporation_rate):
        best_solution = None
        best_score = 0
        for ant in self.ants:
            if ant.get_score_traject(rail_network, ant.traject) > best_score:
                best_score = ant.get_score_traject(rail_network, ant.traject)
                best_solution = ant.traject
        # Evaporate pheromones on all connections
        for connection in self.pheromones:
            self.pheromones[connection] *= (1 - evaporation_rate)
        
        # Update pheromones on connections in the best solution
        for i in range(len(best_solution) - 1):
            connection = (best_solution[i], best_solution[i + 1])
            self.pheromones[connection] += 1 / self.get_score_traject(rail_network, best_solution)

# Initialize parameters
num_ants = 10
num_iterations = 100
evaporation_rate = 0.1




