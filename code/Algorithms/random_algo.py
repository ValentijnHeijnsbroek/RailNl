"""
Random Algorithm for Rail Network Optimization

This script uses a random algorithm to optimize rail trajectories, adhering to constraints 
on the number and duration of trajectories. It iteratively generates and evaluates rail network configurations, 
randomly selecting stations to form each trajectory. 

The goal is to explore the solution space and assess the potential of random configurations 
for network optimization. Scores from each iteration are recorded to understand the variability 
and effectiveness of this approach.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
import copy
from Classes.railnl import RailNL
from typing import List
max_aantal_trajecten: int = 20
max_aantal_minuten: int = 180   

# Create a random procedure to select a amount of trajecten that is less than max aantal trajecten

# Adds a random amount of trajecten to the baseline, each with a random amount of stations. Each station is choosen randomly.
def random_algorithm(herhalingen: int):
    """
    Runs the random algorithm for the specified number of iterations.
    Pre: herhalingen is an integer.
    Post: the score of the random algorithm is returned.
    """
    totaal_herhalingen: int = herhalingen
    baseline_at_max_score: 'RailNL' = RailNL()
    max_score: int = 0
    baseline_at_min_score: 'RailNL' = RailNL()
    min_score: int = 10000
    score_list: List[float] = []
    while herhalingen > 0:
        aantal_trajecten = random.randint(1, max_aantal_trajecten)
        baseline = RailNL()
        baseline.load_stations('StationsNationaal.csv')
        baseline.load_connections('ConnectiesNationaal.csv')
        for i in range(1, aantal_trajecten + 1):
            baseline.create_traject(i)
            random_minuten_per_traject = random.randint(5, max_aantal_minuten)
            begin_station = random.choice(baseline.stations)
            baseline.trajecten[i].add_station_to_traject(begin_station)
            while True:
                if baseline.sum_time(i) < random_minuten_per_traject:
                    # Only possible stations are those in the connections, and those that are not already in the traject
                    list_possible_stations = [station for station in begin_station.connections if not baseline.trajecten[i].is_bereden(station)]
                    if list_possible_stations:
                        new_station = random.choice(list_possible_stations)
                        baseline.trajecten[i].add_station_to_traject(new_station)
                        begin_station = new_station
                    # if there are no possible stations, break the loop
                    else:
                        break
                else:
                    break
        current_score = baseline.get_score()
        score_list.append(current_score)  
        with open('../data/scores/random_scores.txt', 'w') as f:
                for score in score_list:
                    f.write(f"{score}\n")

        herhalingen -= 1 
        if herhalingen/totaal_herhalingen * 100 % 1 == 0:
            print(f"{herhalingen/totaal_herhalingen * 100}%")

    return baseline_at_max_score



# Example usage
baseline = random_algorithm(100)
print(baseline.get_score())
