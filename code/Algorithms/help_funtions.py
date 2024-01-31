""" 
    This file contains all the help functions that are used in the algorithms.
    The functions are:
    - initialize_rail(Map)
    - greedy_decision(rail, traject_index, max_aantal_minuten=180)
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes.railnl import RailNL
import random

def initialize_rail(Map = 'Nationaal'):
    """
    Initializes the rail based on which Map the user wants to use

    pre: Map, Nationaal or Holland
    post Rail initialized based on which map is used
    """
    # The wwhole of the Netherlands
    if Map == 'Nationaal':
        rail_nl = RailNL()
        rail_nl.load_stations('StationsNationaal.csv')
        rail_nl.load_connections('ConnectiesNationaal.csv')
        return rail_nl
    
    # The provinces North and South Holland
    elif Map == "Holland":
        rail_nl = RailNL()
        rail_nl.load_stations('StationsHolland.csv')
        print("test")
        rail_nl.load_connections('ConnectiesHolland.csv')
        print(type(rail_nl))
        return rail_nl

# Takes in a traject and returns the station with the highest delta score
def greedy_decision(rail, traject_index, max_aantal_minuten=180):
    base_score = rail.get_score()
    best_station = None
    latest_station = rail.trajecten[traject_index].traject_stations[-1]
    list_possible_stations = [station for station in latest_station.connections if not rail.trajecten[traject_index].is_visited(station)]
    for station in list_possible_stations:
        rail.trajecten[traject_index].add_station_to_traject(station)
        # If the score is higher than the max score, save the station.
        if rail.get_score() > base_score and rail.sum_time(traject_index) <= max_aantal_minuten:
            base_score = rail.get_score()
            best_station = station
        rail.trajecten[traject_index].delete_station(station)
        # If length of traject = 1 and score is not improved, choose a random possible station
        if len(rail.trajecten[traject_index].traject_stations) == 1:
            best_station = random.choice(list_possible_stations)
    return best_station
