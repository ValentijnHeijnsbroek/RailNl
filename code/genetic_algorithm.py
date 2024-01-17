# main.py

import numpy as np
from railnl import RailNL
import pygad

# Define the fitness function
def fitness_function(ga_instance, solution, solution_idx):
    # Create an instance of the RailNL class
    railnl = RailNL()
    railnl.load_stations('StationsHolland.csv')
    railnl.load_connections('ConnectiesHolland.csv')
    
    # Convert the solution to a valid rail network configuration
    rail_network = railnl.convert_solution(solution)
    
    # Calculate the score based on the rail network configuration
    score = rail_network.get_score()
    
    return score

# genetic_algorithm.py

# ... (import statements)

if __name__ == "__main__":
    railnl = RailNL()
    railnl.load_stations('StationsHolland.csv')
    railnl.load_connections('ConnectiesHolland.csv')

    # Define the number of genes (rail connections) in the solution
    num_genes = railnl.get_num_connections()

    # Define the population size
    population_size = 50

    # Create an instance of the pygad.GA class
    ga_instance = pygad.GA(num_generations=100,
                           num_parents_mating=10,
                           fitness_func=fitness_function,
                           sol_per_pop=population_size,
                           num_genes=num_genes)

    # Run the genetic algorithm
    ga_instance.run()

    # Get the best solution and its fitness value
    best_solution = ga_instance.best_solution()
    best_rail_network = railnl.convert_solution(best_solution, rail_instance=railnl)

    # Print the best rail network
    print("Best Rail Network:", best_rail_network)
    print(best_rail_network.get_score())
    best_rail_network.print_output()


     # Werkt niet,, ben dit nu aan t proberen voor genetic algorithm
    def convert_solution(self, encoded_solution, rail_instance=None, threshold=0.5):
        if rail_instance is None:
            rail_instance = RailNL()

        traject_index = 1
        current_station = None

        # Decode stations and connections
        for index, value in enumerate(encoded_solution):
            # Check if the station is selected
            if value > threshold:
                station_index = index // 2
                if station_index < len(self.stations):
                    station = self.stations[station_index]

                    # Check if the station needs to be added to the current traject
                    if traject_index not in rail_instance.trajecten:
                        rail_instance.create_traject(traject_index)

                    rail_instance.trajecten[traject_index].add_station_to_traject(station)

                    # Update the current station
                    current_station = station

            # Check if a connection should be established
            if index % 2 == 1 and current_station is not None:
                connection_index = index // 2
                if connection_index < self.amount_of_connections:
                    connection_duration = 5
                    # Assuming your connections are stored as pairs of stations
                    other_station = self.stations[connection_index]
                    current_station.add_connection(other_station, connection_duration)

        return rail_instance
    

        # Method that encodes solution to binary, using it as a experiment for genetic algorithm (Vaal)    
    def encode_solution(self):
        # Encode selected stations and connections as binary
        encoded_solution = []

        # Iterate over trajecten
        for traject_index in range(1, self.max_trajecten + 1):
            # Create a set of selected stations for each traject
            selected_stations = set(station for station in self.trajecten[traject_index].traject_stations)

            # Encode stations as binary (1 if selected, 0 if not)
            for station in self.stations:
                if station in selected_stations:
                    encoded_solution.append(1)
                else:
                    encoded_solution.append(0)

                # Encode the number of connections for each station
                encoded_solution.append(len(station.connections))

        return np.array(encoded_solution)
