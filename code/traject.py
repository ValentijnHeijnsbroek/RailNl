import csv
from station import Station
from connections import Connections

class Traject:
    
    def __init__(self):
        self.duration = 0
        self.traject_stations = []

        # test list
        # self.stations = ['Amsterdam Amstel', 'Amsterdam Zuid']
    def add_station_to_traject(self, station: Station, station_connection: dict[Station, list[Station]]):
        """
        Here the stations are added to the traject and it adds the first station inside of the list to the traject

        """
        if station in station_connection:
            connected_stations = station_connection[station]
            if connected_stations:
                first_connected_station = connected_stations[0]
                self.traject_stations.append(first_connected_station)
    
    def get_time(self, connection_distance: dict[(Station, Station), float]):
        """
        here the duration is added between the stations of the traject until it reaches the trajects end
        """
        for i in range(len(self.traject_stations) - 1):
            station1 = self.traject_stations[i]
            station2 = self.traject_stations[i + 1]
            connection_key = (station1, station2)

            if connection_key in connection_distance:
                self.duration += connection_distance[connection_key]


# class Traject():
#     def __init__(self):
#         self.stations = []

#     def add_station(self, station):
#         self.stations.append(station)
        
#     def calculate_duration(self):
#         duration = 0
#         for i in range(len(self.stations) - 1):
#             current_station = self.stations[i]
#             next_station = self.stations[i + 1]
#             duration += current_station.connections[next_station]
#         return duration


# class Traject:
#     stations = []
#     def __init__(self, traject_stations: list, traject_duration: int):
#         self.traject_stations = traject_stations
#         self.duration = 0
        
#     def add_station(self, station):
#         if not self.has_station(station):
#             self.stations.append(station)

#     def delself._station(self, station):
#         if self.has_station(station):
#             self.stations.remove(station)
        
#     def has_station(self, station):
#         return station in self.stations   
    
#     def get_station_names(self):
#         return [station.get_name() for station in self.stations]
    
    