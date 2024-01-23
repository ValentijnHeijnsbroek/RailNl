from railnl import RailNL
import random
import math
import copy
from help_funtions import *
from greedy import greedy_algorithm

max_aantal_trajecten = 20
max_aantal_minuten = 180

def hill_climber(iterations, greedy_iterations=1000):
    rail_at_max_score = initialize_rail("Nationaal")
    current_rail = initialize_rail("Nationaal")
    best_score = 0

    for iteration in range(iterations):
        # Print progress of iterations
        if iteration/iterations * 100 % 10 == 0:
            print(f"{iteration/iterations * 100}%")
  
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

    return rail_at_max_score

def generate_new_solution(current_rail, greedy_iterations):
    if len(current_rail.trajecten) <= 1:
        new_rail = greedy_algorithm(greedy_iterations)
        # new_rail.print_output()
        print("Greedy successfully loaded, greedy has a score of: ", new_rail.get_score())
    else:
        new_rail = copy.deepcopy(current_rail)

    operation = random.choice(['add_station', 'delete_station'])

    traject_index = random.randint(1, len(new_rail.trajecten))

    #if selected traject is empty, add a random station
    if new_rail.trajecten[traject_index].traject_stations == []:
        begin_station = random.choice(new_rail.stations)
        new_rail.trajecten[traject_index].add_station_to_traject(begin_station)

    
    if operation == 'add_station':
        # Implement logic to add a station to an existing traject
  
        new_station = new_rail.trajecten[traject_index].random_connected_station()
        last_station = new_rail.trajecten[traject_index].last_station()
        # duration = last_station.get_duration(new_station)
        duration = last_station.get_duration(new_station)

        # Check if the new station can be added to the traject
        if new_station and new_rail.sum_time(traject_index) + duration <= max_aantal_minuten:
            new_rail.trajecten[traject_index].add_station_to_traject(new_station)
        else:
            operation = 'delete_station'

    elif operation == 'delete_station':
        # Implement logic to delete a station from an existing traject
        if new_rail.trajecten[traject_index].traject_stations:
            new_rail.trajecten[traject_index].delete_latest_station()

    # Randomly select a traject to modify
    if len(new_rail.trajecten) == 1:
        traject_index = 1
    elif len(new_rail.trajecten) == 0:
        new_rail.create_traject(1)
        traject_index = 1
    elif len(new_rail.trajecten) > 1:
        traject_index = random.randint(1, len(new_rail.trajecten))

   # Delete the last two stations if the traject is longer than 3 stations, then pick a random station and a greedy station
    traject = new_rail.trajecten[traject_index]
    if len(traject.traject_stations) > 3:
        traject.delete_latest_station()
        traject.delete_latest_station()
        random_station = traject.random_connected_station()
        if random_station:
            traject.add_station_to_traject(random_station)
        greedy_station_2 = greedy_decision(new_rail, traject_index)
        if greedy_station_2:
            traject.add_station_to_traject(greedy_station_2)
    
    elif len(traject.traject_stations) <= 3:
        traject.traject_stations = []
        # traject.delete_latest_station()
        # random_station = traject.random_connected_station()
        # traject.add_station_to_traject(random_station)
        
    return new_rail

# Print and save the best rail from the hill climber


def run_hill_climber(num_runs, iterations, greedy_iterations=1000):
    best_rail = None
    best_score = 0

    for run in range(1, num_runs + 1):
        print(f"Run {run}/{num_runs}")

        rail_at_max_score = hill_climber(iterations, greedy_iterations)
        current_score = rail_at_max_score.get_score()

        print(f"Score for run {run}: {current_score}")

        if current_score > best_score:
            best_score = current_score
            best_rail = copy.deepcopy(rail_at_max_score)

    return best_rail

# Set parameters for the hill climber
hill_climber_iterations = 1000
hill_climber_greedy_iterations = 1000
num_runs_hill_climber = 10 # Specify the number of runs

# Run the hill climber algorithm and get the best rail
best_rail_hill_climber = run_hill_climber(num_runs_hill_climber, hill_climber_iterations, hill_climber_greedy_iterations)

# Print and save the best rail from the hill climber
if best_rail_hill_climber is not None:
    print("Best Rail (Hill Climber):")
    best_rail_hill_climber.print_output()
    best_rail_hill_climber.upload_output('output_hill_climber.csv')