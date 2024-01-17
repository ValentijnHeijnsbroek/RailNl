from railnl import RailNL
import random

def initialize_rail():
    rail_nl = RailNL()
    rail_nl.load_stations('StationsNationaal.csv')
    rail_nl.load_connections('ConnectiesNationaal.csv')
    return rail_nl

# Takes in a traject and returns the station with the highest delta score
def greedy_decision(rail, traject_index, max_aantal_minuten=180):
    base_score = rail.get_score()
    best_station = None
    latest_station = rail.trajecten[traject_index].traject_stations[-1]
    list_possible_stations = [station for station in latest_station.connections if not rail.trajecten[traject_index].is_bereden(station)]
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
