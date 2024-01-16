from greedy import *
from random_algo import *

def run_random_algorithm(iterations):
    # Code for running the random algorithm
    print(f"Running random algorithm for {iterations} iterations...")
    random_output = random_algorithm(iterations)
    return print(random_output.get_score())

def run_greedy_algorithm(iterations):
    # Code for running the greedy algorithm
    print(f"Running greedy algorithm for {iterations} iterations...")
    greedy_output = greedy_algorithm(iterations)
    return print(greedy_output.get_score())

# Ask for user input
algorithm = input("Enter 'R' to run the random algorithm, 'G' to run the greedy algorithm, or 'B' to run both: ")
iterations = int(input("Enter the number of iterations: "))

# Run the algorithm(s)
if algorithm == 'R':
    run_random_algorithm(iterations)
elif algorithm == 'G':
    run_greedy_algorithm(iterations)
elif algorithm == 'B':
    print(f"Running both algorithms for {iterations} iterations...")
    print(f"First running random algorithm for {iterations} iterations...")
    random_output = random_algorithm(iterations)
    print(f"Random alforithm complete. Now running greedy algorithm for {iterations} iterations...")
    greedy_output = greedy_algorithm(iterations)
    print("Random algorithm score:", random_output.get_score())
    print("Greedy algorithm score:", greedy_output.get_score())
else:
    print("Invalid input. Please enter 'R', 'G', or 'B'.")
