from railnl import RailNL
import random
from station import Station
import copy
from help_funtions import *
max_aantal_trajecten = 20
max_aantal_minuten = 180

def greedy_algorithm(herhalingen):
    totaal_herhalingen = herhalingen
    greedy_at_max_score = initialize_rail()
    greedy = initialize_rail()
    max_score = 0
    while herhalingen > 0:
        aantal_trajecten = random.randint(1, max_aantal_trajecten)
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

        # for own reference if highscore is beaten
        if greedy.get_score() > 7300.14:
            print(greedy.get_score())
        # If the score is higher than the max score, save trajecten
        if greedy.get_score() > max_score:
            max_score = greedy.get_score()
            greedy_at_max_score.trajecten = greedy.trajecten
        herhalingen -= 1
        # print progress
        if herhalingen/totaal_herhalingen * 100 % 5 == 0:
            print(f"{herhalingen/totaal_herhalingen * 100}%")
        greedy.trajecten = {}
    return greedy_at_max_score

greedy = greedy_algorithm(10000)
greedy.print_output()