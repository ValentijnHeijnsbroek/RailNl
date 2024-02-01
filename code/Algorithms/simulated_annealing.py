"""
Simulated Annealing Algorithm for Rail Network Optimization

This script implements the simulated annealing algorithm to optimize a rail network configuration. 
The optimization includes adding, deleting, and substituting stations in trajectories to maximize the overall score. 
The algorithm uses a greedy algorithm to get a base state.

"""
import sys
import time
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes.railnl import RailNL
from Classes.station import Station
from Classes.traject import Traject

import random
import math
import copy

import matplotlib.pyplot as plt
from itertools import product
from help_funtions import initialize_rail, greedy_decision  
from greedy import greedy_algorithm
import time

max_aantal_trajecten: int = 20
max_aantal_minuten: int = 180
max_iterations_without_improvement: int = 3000

def simulated_annealing(temperature: float, cooling_rate: float, iterations: int, 
                        greedy_iterations: int = 1000, min_aantal_trajecten: int = 5, 
                        new_solution_iterations: int = 1) -> RailNL:
    """
    Run simulated annealing algorithm.

    Pre: temperature (float): Initial temperature for simulated annealing
         cooling_rate (float): Cooling rate for simulated annealing
         iterations (int): Number of iterations for simulated annealing
         greedy_iterations (int): Number of iterations for the greedy algorithm within each iteration of simulated annealing
         min_aantal_trajecten (int): Minimum number of trajectories
         new_solution_iterations (int): Number of iterations to generate a new solution
    Post: RailNL: Best RailNL object obtained through simulated annealing
    """
    rail_at_max_score: RailNL = initialize_rail("Nationaal")
    current_rail: RailNL = initialize_rail("Nationaal")
    best_score: int = 0
    iterations_list: list[int] = []
    scores_list: list[int] = []
    iterations_without_improvement: int = 0

    for iteration in range(iterations):
        current_temperature: float = temperature * math.exp(-cooling_rate * iteration)

        # Generate a new solution
        for i in range(new_solution_iterations):
            if i == 0:
                new_rail: RailNL = generate_new_solution(current_rail, greedy_iterations, min_aantal_trajecten)
            else:
                new_rail: RailNL = generate_new_solution(new_rail, greedy_iterations, min_aantal_trajecten)

        # Calculate scores
        current_score: int = current_rail.get_score()
        new_score: int = new_rail.get_score()

        iterations_list.append(iteration)
        scores_list.append(new_score)

        # Decide whether to accept the new solution
        if accept_solution(current_score, new_score, current_temperature):
            current_rail = new_rail

            # Update the best solution if needed
            if new_score > best_score:
                best_score = new_score
                rail_at_max_score.trajecten = current_rail.trajecten
                iterations_without_improvement = 0
            else:
                iterations_without_improvement += 1 
        
        if iterations_without_improvement >= max_iterations_without_improvement and iteration > 1000:
            print(f"Breaking out of the loop due to no improvement in {max_iterations_without_improvement} iterations.")
            break
    
    # For plotting purposes
    rail_at_max_score.iterations_list = iterations_list
    rail_at_max_score.scores_list = scores_list
    return rail_at_max_score

def generate_new_solution(current_rail: RailNL, greedy_iterations: int, min_aantal_trajecten: int) -> RailNL:
    """
    Generate a new solution based on the current rail.

    Pre: current_rail (RailNL): Current RailNL object
         greedy_iterations (int): Number of iterations for the greedy algorithm
         min_aantal_trajecten (int): Minimum number of trajectories
    Post: RailNL: New RailNL object
    """
    if len(current_rail.trajecten) <= 1:
        new_rail: RailNL = greedy_algorithm(greedy_iterations, min_aantal_trajecten)
        print("Greedy successfully loaded, greedy has a score of: ", new_rail.get_score())
    else:
        new_rail: RailNL = copy.deepcopy(current_rail)
        
    operation: str = random.choice(['add_station', 'delete_station', 'substitute_stations'])
    traject_index: int = random.randint(1, len(new_rail.trajecten))

    # If selected traject is empty, add a random station
    if new_rail.trajecten[traject_index].traject_stations == []:
        begin_station: Station = random.choice(new_rail.stations)
        new_rail.trajecten[traject_index].add_station_to_traject(begin_station)
    
    if operation == 'add_station':
        new_station: Station = new_rail.trajecten[traject_index].random_connected_station()
        last_station: Station = new_rail.trajecten[traject_index].last_station()
        duration: float = last_station.get_duration(new_station)

        # Check if the new station can be added to the traject
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
        traject: Traject = new_rail.trajecten[traject_index]

        if len(traject.traject_stations) >= 3:
            traject.delete_latest_station()
            traject.delete_latest_station()
            random_station: Station = traject.random_connected_station()

            if random_station:
                traject.add_station_to_traject(random_station)

            greedy_station_2: Station = greedy_decision(new_rail, traject_index)
            
            if greedy_station_2:
                traject.add_station_to_traject(greedy_station_2)
    
    return new_rail

def accept_solution(current_score: int, new_score: int, temperature: float) -> bool:
    """
    Accepts or rejects a new solution based on the Metropolis criterion.

    Pre: current_score (int): Current score
         new_score (int): New score
         temperature (float): Current temperature
    Post:bool: True if the new solution is accepted, False otherwise
    """
    if new_score > current_score:
        return True
    else:
        probability: float = math.exp((new_score - current_score) / temperature)
        return random.uniform(0, 1) < probability
    
def run_simulated_annealing(num_runs: int, temperature: float, cooling_rate: float, iterations: int, 
                            greedy_iterations: int = 1000, min_aantal_trajecten: int = 5, 
                            new_solution_iterations: int = 1, max_time: int = 0) -> RailNL:
    """
    Run simulated annealing multiple times and return the best rail.

    Pre: num_runs (int): Number of runs
         temperature (float): Initial temperature for simulated annealing
         cooling_rate (float): Cooling rate for simulated annealing
         iterations (int): Number of iterations for simulated annealing
         greedy_iterations (int): Number of iterations for the greedy algorithm within each iteration of simulated annealing
         min_aantal_trajecten (int): Minimum number of trajectories
         new_solution_iterations (int): Number of iterations to generate a new solution
         max_time (int): Maximum time in seconds, if reached, exit the loop
    Post: RailNL: Best RailNL object obtained through simulated annealing
    """
    best_rail: RailNL = None
    best_score: int = 0
    scores_list: list[int] = []
    start_time = time.time()

    for run in range(1, num_runs + 1):
        print(f"Run {run}/{num_runs}, best score == {best_score}")

        rail_at_max_score: RailNL = simulated_annealing(
            temperature, cooling_rate, iterations, greedy_iterations, 
            min_aantal_trajecten=min_aantal_trajecten, new_solution_iterations=new_solution_iterations
        )
        current_score: int = rail_at_max_score.get_score()
        scores_list.append(current_score)
        # to save data in a txt file to compare in a histogram
        with open('../data/scores/simulated_annealing_scores.txt', 'w') as file:
            for score in scores_list:
                file.write(f"{score}\n")

        print(f"Score for run {run}: {current_score}")

        if run/num_runs * 100 % 10 == 0:
            print(f"Best score at {run/num_runs * 100}% == {best_score}")

        if current_score > best_score:
            best_score = current_score
            best_rail = copy.deepcopy(rail_at_max_score)

        # Check if maximum time is reached
        if max_time > 0 and time.time() - start_time >= max_time:
            print("Maximum time reached. Exiting the loop.")
            break

    # Iteration and scores list for visualization
    iterations_process_list: list[int] = best_rail.iterations_list
    scores_process_list: list[int] = best_rail.scores_list

    plt.figure(figsize=(10, 6))
    plt.plot(iterations_process_list, scores_process_list, label="Score")
    plt.xlabel("Iterations")
    plt.ylabel("Score")
    plt.title("Simulated Annealing Progress")
    plt.legend()
    plt.axhline(y=best_score, color='red', linestyle='--', label=f'Max Score: {best_score}')
    plt.savefig('pics/Simulated_Annealing_process.png')
    plt.close()

    # Calculate average score
    if num_runs > 5:   
        average_score: float = sum(scores_list) / len(scores_list)

        # Show distribution
        bin_width: int = 50
        num_bins: int = int((max(scores_list) - min(scores_list)) / bin_width)

        plt.figure(figsize=(10, 6))
        plt.hist(scores_list, bins=num_bins, color='blue', edgecolor='black')
        plt.axvline(x=best_score, color='red', linestyle='--', label=f'Highest Score: {best_score}')
        plt.xlabel('Score')
        plt.ylabel('Frequency')
        plt.title(f"Simulated Annealing Progress\nInitial Temperature: {temperature}, Cooling Rate: {cooling_rate}, Iterations: {iterations}, num_runs: {num_runs}\n Average Score: {average_score}")
        plt.legend()
        plt.savefig('pics/Score_Distribution_Simulated_Annealing_Clustered.png')

    return best_rail


num_runs = 100000
initial_temperature = 1000
cooling_rate = 0.005
iterations = 1500
min_aantal_trajecten = 10
greedy_iterations = 500
new_solution_iterations = 1
max_time = 1200


# Run simulated annealing multiple times and get the best rail
best_rail = run_simulated_annealing(num_runs, initial_temperature, cooling_rate, iterations, greedy_iterations, min_aantal_trajecten, new_solution_iterations = new_solution_iterations, max_time = max_time)

# Print and save the best rail
if best_rail is not None:
    print("Best Rail:")
    if(best_rail.get_score() > 6735):
        print("New HighScore!")
        best_rail.print_output()
        best_rail.upload_output('Highscore_simulated_annealing.csv')
    else:
        best_rail.print_output()
        best_rail.upload_output('output_simulated_annealing.csv')

