from railnl import RailNL

def initialize_rail():
    rail_nl = RailNL()
    rail_nl.load_stations('StationsNationaal.csv')
    rail_nl.load_connections('ConnectiesNationaal.csv')
    return rail_nl

# Takes in a traject and returns the station with the highest delta score
def greedy_decision(rail, traject_index):

    base_score = rail.get_score()
    best_station = None
    latest_station = rail.trajecten[traject_index].traject_stations[-1]
    list_possible_stations = [station for station in latest_station.connections if not rail.trajecten[traject_index].is_bereden(station)]
    for station in list_possible_stations:
        rail.trajecten[traject_index].add_station_to_traject(station)
        rail.get_score()
        # If the score is higher than the max score, save the station.
        if rail.get_score() > base_score:
            base_score = rail.get_score()
            best_station = station
        rail.trajecten[traject_index].delete_station(station)
    return best_station
