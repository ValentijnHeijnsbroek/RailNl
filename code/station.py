import csv
class Station:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

        self.connections = set()
        self.connections_durations = {}
    
    def add_connection(self, station, duration):
        self.connections.add(station)
        self.connections_durations[station] = duration

    def has_connection(self, station):
        return station in self.connections
    
    def get_duration(self, station):
        return self.connections_durations[station]
