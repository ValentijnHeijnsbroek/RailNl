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