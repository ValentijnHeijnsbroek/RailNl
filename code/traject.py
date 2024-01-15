import csv
from station import Station
from connections import Connections

class Traject:
    def __init__(self):
        self.duration = 0
        self.traject_stations = []
    
    def add_station_to_traject(self, station: Station):
        """
        Add stations to the traject, if it was already in the traject list it goes to the next one that is connected to the 
        given station.
        """
        
        if len(self.traject_stations) == 0:
            self.traject_stations.append(station)
        else:
            last_station = self.traject_stations[-1]
        
            if station in last_station.connections:
                self.traject_stations.append(station)
            else:
               print("ERROR: Station not in connection with traject")


    
        # connected_stations = stations_connections[station]        
        # for connected_station in connected_stations:
        #     if connected_station not in self.traject_stations:
        #         self.traject_stations.append(connected_station)
        #         break


    def get_time(self, connections):
        """
        Here the duration is added between the stations of the traject until it reaches the traject's end
        """
        for i in range(len(self.traject_stations) - 1):
            station1 = self.traject_stations[i]
            station2 = self.traject_stations[i + 1]
            connection_key = (station1, station2)

            if connections.has_connection(connection_key):
                self.duration += connections.get_duration(connection_key)



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
    
    