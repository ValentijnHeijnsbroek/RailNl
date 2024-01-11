class Traject():
    def __init__(self):
        self.stations = []

    def add_station(self, station):
        self.stations.append(station)
        
    def calculate_duration(self):
        duration = 0
        for i in range(len(self.stations) - 1):
            current_station = self.stations[i]
            next_station = self.stations[i + 1]
            duration += current_station.connections[next_station]
        return duration


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
    
    