"""
Hill Climber Algorithm for Rail Network Optimization

This script implements the hill climber algorithm to optimize a rail network configuration. 
The optimization includes adding, deleting, and substituting stations in trajectories to maximize the overall score. 
The algorithm uses a combination of hill climbing and a greedy algorithm for trajectory generation.

"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes.railnl import RailNL
import random
import copy
import matplotlib.pyplot as plt 
import time
from help_funtions import initialize_rail, greedy_decision
from greedy import greedy_algorithm
from typing import List


max_aantal_trajecten: int = 20
max_aantal_minuten: int = 180

def hill_climber(iterations: int, greedy_iterations: int = 1000) -> RailNL:
    """
    Perform hill climber algorithm  to optimize a rail network configuration.

    Pre: iterations (int): Number of iterations for the hill climber algorithm.
         greedy_iterations (int): Number of iterations for the greedy algorithm.

    Post: RailNL: Best rail configuration found by the algorithm.
    """
    rail_at_max_score: RailNL = initialize_rail("Nationaal")
    current_rail: RailNL = initialize_rail("Nationaal")
    best_score: int = 0
    scores_list: List[int] = []
    iterations_list: List[int] = []

    for iteration in range(iterations):
        # Print progress of iterations
        # if iteration / iterations * 100 % 10 == 0:
        #     print(f"{iteration / iterations * 100}%")

        # Generate a new solution
        new_rail = generate_new_solution(current_rail, greedy_iterations)

        # Calculate scores
        current_score = current_rail.get_score()
        new_score = new_rail.get_score()

        # If the new solution has a higher score, update the current rail
        if new_score > current_score:
            current_rail = copy.deepcopy(new_rail)
            # Update the best solution if needed
            if new_score > best_score:
                best_score = new_score
                rail_at_max_score.trajecten = copy.deepcopy(current_rail.trajecten)

        scores_list.append(best_score)
        iterations_list.append(iteration)

    return rail_at_max_score

def generate_new_solution(current_rail: RailNL, greedy_iterations: int) -> RailNL:
    """
    Generate a new rail configuration by applying operations like adding, deleting, or substituting stations.

    Pre: current_rail (RailNL): Current rail configuration.
         greedy_iterations (int): Number of iterations for the greedy algorithm.
    Post: RailNL: New rail configuration.
    """
    if len(current_rail.trajecten) <= 1:
        new_rail = greedy_algorithm(greedy_iterations)
        print("Greedy successfully loaded, greedy has a score of: ", new_rail.get_score())
    else:
        new_rail = copy.deepcopy(current_rail)

    operation = random.choice(['add_station', 'delete_station', 'substitute_stations'])

    traject_index = random.randint(1, len(new_rail.trajecten))

    # If selected traject is empty, add a random station
    if new_rail.trajecten[traject_index].traject_stations == []:
        begin_station = random.choice(new_rail.stations)
        new_rail.trajecten[traject_index].add_station_to_traject(begin_station)

    if operation == 'add_station':
        new_station = new_rail.trajecten[traject_index].random_connected_station()
        last_station = new_rail.trajecten[traject_index].last_station()
        duration = last_station.get_duration(new_station)
        if new_station and new_rail.sum_time(traject_index) + duration <= max_aantal_minuten:
            new_rail.trajecten[traject_index].add_station_to_traject(new_station)
        else:
            operation = 'substitute_stations'

    elif operation == 'delete_station':
        traject_index = random.randint(1, len(new_rail.trajecten))
        if new_rail.trajecten[traject_index].traject_stations:
            new_rail.trajecten[traject_index].delete_latest_station()

    elif operation == 'substitute_stations':
        traject_index = random.randint(1, len(new_rail.trajecten))
        traject = new_rail.trajecten[traject_index]
        if len(traject.traject_stations) >= 3:
            traject.delete_latest_station()
            traject.delete_latest_station()
            random_station = traject.random_connected_station()
            if random_station:
                traject.add_station_to_traject(random_station)
            greedy_station_2 = greedy_decision(new_rail, traject_index)
            if greedy_station_2:
                traject.add_station_to_traject(greedy_station_2)

    return new_rail

def run_hill_climber(num_runs: int, iterations: int, greedy_iterations: int = 1000, max_time = 0) -> RailNL:
    """
    Run the hill climber algorithm multiple times and return the best rail configuration.

    Pre: num_runs (int): Number of runs for the hill climber algorithm.
         iterations (int): Number of iterations for each run of the hill climber algorithm.
         greedy_iterations (int): Number of iterations for the greedy algorithm.
    Post:  RailNL: Best rail configuration found across multiple runs.
    """
    best_rail: RailNL = None
    best_score: int = 0
    scores_list: List[int] = []
    start_time = time.time()

    for run in range(1, num_runs + 1):
        print(f"Run {run}/{num_runs}")

        rail_at_max_score = hill_climber(iterations, greedy_iterations)
        current_score = rail_at_max_score.get_score()
        scores_list.append(current_score)

        print(f"Score for run {run}: {current_score}")
        with open('../data/scores/hill_climber_scores.txt', 'w') as file:
            for score in scores_list:
                file.write(f"{score}\n")

        if current_score > best_score:
            best_score = current_score
            best_rail = copy.deepcopy(rail_at_max_score)

        if max_time > 1 and time.time() - start_time >= max_time:
            break

    return best_rail

# Set parameters for the hill climber
hill_climber_iterations = 1000
hill_climber_greedy_iterations = 600
num_runs_hill_climber = 100000  # Specify the number of runs
max_time = 1200

# Run the hill climber algorithm and get the best rail
best_rail_hill_climber = run_hill_climber(num_runs_hill_climber, hill_climber_iterations, hill_climber_greedy_iterations, max_time=max_time)

# Print and save the best rail from the hill climber
if best_rail_hill_climber is not None:
    print("Best Rail (Hill Climber):")
    best_rail_hill_climber.print_output()
    best_rail_hill_climber.upload_output('output_hill_climber.csv')


