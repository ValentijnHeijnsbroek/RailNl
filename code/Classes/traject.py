from .station import Station
from typing import Any
import random

class Traject:
    def __init__(self):
        """
        Initializes an empty Traject object with zero duration and no traject stations.
        """
        self.duration: float = 0
        self.traject_stations: list[Station] = []

    
    def add_station_to_traject(self, station: Station) -> None:
        """
        Add stations to the traject. If it was already in the traject list, it goes to the next one that is connected to the given station.

        pre: station object to add to the traject
        post: if the traject is empty, station is added to the traject_stations list.
              if it isnt empty a connected station is added to the list and if it isnt in 
              the traject already
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
    
    def is_visited(self, station: Station) -> bool:
        """
        Checks if a given station is already present in the traject.

        pre: station object
        post: bool like that give true if the station is in the traject_stations list and 
              false if it isnt there
        """
        return station in self.traject_stations
    
    def delete_station(self, station: Station) -> None:
        """
        Deletes a specific station from the traject_stations list if it exists in the list.

        pre: station object 
        post: removes the station if it is in the traject_stations list
        """
        if station in self.traject_stations:
            self.traject_stations.remove(station)
    
    def delete_latest_station(self) -> None:
        """
        Deletes the latest station from the traject_stations list, 
        if the traject_stations list is not empty

        post: traject deletes the latest station added if the traject_stations list in not empty
        """
        if self.traject_stations:
            self.traject_stations.pop()

    # Returns a random connected station
    def random_connected_station(self) -> Any:
        """
        Returns a random connected station to the last station in the traject_stations list.

        post: if the traject is empty, 'station' is added to the traject_stations list.
              if the traject_stations list is not empty and there are connected stations to the last station, a random connected station is returned.    
        """
        # Checks what connections the station has
        if self.traject_stations:
            last_station = self.traject_stations[-1]
            list_possible_stations = [station for station in last_station.connections if not self.is_visited(station)]
            if list_possible_stations:
                random_station = random.choice(list_possible_stations)
                return random_station
            else:
                return None
        else:
            print("Cannot add a random station to an empty traject.")
            return None

    def last_station(self) -> Any:
        """
        Returns the last station in the traject_stations list.

        post: returns lastest addition to the traject if the traject_stations list isnt empty
              otherwise it returns None 
        """
        if self.traject_stations:
            return self.traject_stations[-1]
        else:
            return None