import csv
from station import Station
import random

class Traject:
    def __init__(self):
        self.duration = 0
        self.traject_stations = []

        # last_station = self.traject_stations[-1]
        # self.list_possible_stations = [station for station in last_station.connections if not self.is_bereden(station)]

    
    def add_station_to_traject(self, station: Station):
        """
        Add stations to the traject, if it was already in the traject list it goes to the next one that is connected to the 
        given station.
        """
        
        if len(self.traject_stations) == 0:
            self.traject_stations.append(station)
        else:

            last_station = self.traject_stations[-1]


            if station in last_station.connections and station not in self.traject_stations:
                self.traject_stations.append(station)
            else:
                if station in self.traject_stations:
                   print(f"ERROR: Station {station.name} already in traject")
                elif station not in last_station.connections:
                    print(f"ERROR: Station {station.name} not in connection with traject")
    
    def is_bereden(self, station):
        return station in self.traject_stations
    
    def delete_station(self, station):
        if station in self.traject_stations:
            self.traject_stations.remove(station)
    
    def delete_latest_station(self):
        if self.traject_stations:
            self.traject_stations.pop()
        else:
            #print("Cannot delete from an empty list.")
            pass

    # Returns a random connected station
    def random_connected_station(self):
        if self.traject_stations:
            last_station = self.traject_stations[-1]
            list_possible_stations = [station for station in last_station.connections if not self.is_bereden(station)]
            if list_possible_stations:
                
                random_station = random.choice(list_possible_stations)
                return random_station
            else:
                # print("No connections")
                return None
        else:
            print("Cannot add random station to an empty traject.")
            return None

    def last_station(self):
        return self.traject_stations[-1]    
    
