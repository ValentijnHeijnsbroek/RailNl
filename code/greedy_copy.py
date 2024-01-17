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
                list_possible_stations = [station for station in begin_station.connections if not greedy.trajecten[i].is_bereden(station)]
                max_score_station = 0
                if list_possible_stations:
                    best_station = None
                    for station in list_possible_stations:
                        greedy.trajecten[i].add_station_to_traject(station)
                        greedy.get_score()
                        # If the score is higher than the max score, save the station.
                        if greedy.get_score() > max_score_station:
                            max_score_station = greedy.get_score()
                            best_station = station
                        greedy.trajecten[i].delete_station(station)

                    # if best_station exists and it contributes to the score, add the station to the traject
                    if best_station and max_score_station > 0:
                        greedy.trajecten[i].add_station_to_traject(best_station)
                    else:
                        break
                    begin_station = best_station

                # if there are no possible stations, break the loop 
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




# railnl_at_max_score = greedy_algorithm(1000)
# railnl_at_max_score.print_output()
# railnl_at_max_score.upload_output('output_greedy.csv')

