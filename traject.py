class Traject:
    stations = []
    def __init__(self, traject_stations: list, traject_duration: int):
        self.traject_stations = traject_stations
        self.duration = 0
        
    def add_station(self, station):
        if not self.has_station(station):
            self.stations.append(station)

    def delself._station(self, station):
        if self.has_station(station):
            self.stations.remove(station)
        
    def has_station(self, station):
        return station in self.stations   
    
    def get_station_names(self):
        return [station.get_name() for station in self.stations]
    
    