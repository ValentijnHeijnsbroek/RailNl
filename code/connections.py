from station import Station
import csv

class Connections:
    def __init__(self):
        self.connections = {}

    def add_connection(self, station1, station2, duration):
        """
        Here the connections dictionary is used to create a key tuple where the values
         are station 1 and station 2, and the value is the duration of getting from station(1/2)
         to station(2/1)
        """
        self.connections[(station1, station2)] = duration
        self.connections[(station2, station1)] = duration

    def has_connection(self, station1, station2):
        return (station1, station2) in self.connections

    def get_duration(self, station1, station2):
        """
        used to get the duration 
        """
        return self.connections.get((station1, station2), float('inf'))


