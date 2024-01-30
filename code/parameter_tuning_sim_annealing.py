from railnl import RailNL
from itertools import product
from help_funtions import *
from simulated_annealing import run_simulated_annealing

def perform_grid_search():
    """
    Perform a grid search for simulated annealing parameters.
    """
    initial_temperatures: list[int] = [600, 800, 1000, 1200]
    cooling_rates: list[float] = [0.005, 0.004, 0.003]

    # Results dictionary to store the best rail for each parameter combination
    results: dict[tuple[int, float], tuple[RailNL, int]] = {}

    for temp, rate in product(initial_temperatures, cooling_rates):
        print(f"Testing parameters: Initial Temperature = {temp}, Cooling Rate = {rate}")
        
        # Run simulated annealing multiple times and get the best rail for each combination
        best_rail: RailNL = run_simulated_annealing(
            num_runs=200,
            temperature=temp,
            cooling_rate=rate,
            iterations=1500,
            greedy_iterations=300,
            min_aantal_trajecten=10,
            new_solution_iterations=2
        )

        # Store the best rail and its score in the results dictionary
        results[(temp, rate)] = (best_rail, best_rail.get_score())

        # Print the score for the current combination
        print(f"Score for parameters ({temp}, {rate}): {best_rail.get_score()}")

    print("\nScores of all parameters:")
    for (temp, rate), (rail, score) in results.items():
        print(f"({temp}, {rate}): {score}", end=", ")

    # Print the best rail and its score
    best_params, (best_rail, best_score) = max(results.items(), key=lambda x: x[1][1])
    print(f"\nBest Rail (Parameters: Initial Temperature = {best_params[0]}, Cooling Rate = {best_params[1]}):")
    print(f"Score: {best_score}")

perform_grid_search()
