import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes.railnl import RailNL
import random
from Classes.station import Station
import copy
from help_funtions import *
from typing import List

max_aantal_trajecten = 20
max_aantal_minuten = 180
#Toevoegen dat traject begint bij een station met weinig verbindingen bijv

def greedy_algorithm(herhalingen, min_aantal_trajecten = 5):
    totaal_herhalingen = herhalingen
    greedy_at_max_score = initialize_rail("Nationaal")
    greedy = initialize_rail("Nationaal")
    max_score = 0
    score_list: List[float] = []
    while herhalingen > 0:
        aantal_trajecten = random.randint(min_aantal_trajecten, max_aantal_trajecten)
        for i in range(1, aantal_trajecten + 1):
            greedy.create_traject(i)
            begin_station = random.choice(greedy.stations)
            greedy.trajecten[i].add_station_to_traject(begin_station)
            max_score_station = 0
            while max_score_station >= 0 and greedy.sum_time(i) < max_aantal_minuten:
                new_station = greedy_decision(greedy, traject_index=i)
                if new_station:
                    greedy.trajecten[i].add_station_to_traject(new_station)
                    # If length of traject == 1 and new_station is None, choose a new random begin station
                elif len(greedy.trajecten[i].traject_stations) == 1 and new_station is None:
                        greedy.trajecten[i].delete_station(greedy.trajecten[i].traject_stations[0])
                        begin_station = random.choice(greedy.stations)
                        greedy.trajecten[i].add_station_to_traject(begin_station)
                else:    
                    break
        current_score = greedy.get_score()
        score_list.append(current_score)  
        with open('../data/greedy_scores.txt', 'w') as f:
                for score in score_list:
                    f.write(f"{score}\n")

        # for own reference if highscore is beaten
        if greedy.get_score() > max_score:
            max_score = greedy.get_score()
            greedy_at_max_score.trajecten = greedy.trajecten
        herhalingen -= 1
        # print progress
        # if herhalingen/totaal_herhalingen * 100 % 25 == 0:
        #     print(f"{herhalingen/totaal_herhalingen * 100}%")
        greedy.trajecten = {}
    return greedy_at_max_score

greedy = greedy_algorithm(100)
greedy.print_output()