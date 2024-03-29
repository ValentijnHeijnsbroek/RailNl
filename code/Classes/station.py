"""
Station Class
This script introduces a Station class representing a train station. 
The class encapsulates essential attributes such as the station's name and coordinates (x, y). 
The key functionalities include adding connections with durations, checking for existing connections, and retrieving connection durations.

"""

from typing import Any

class Station:
    """
    Represents a train station.

    """

    def __init__(self, name: str, x: float, y: float):
        """
        Initializes a new Station object, with coordinates.
        initializes a connections set and a connection duration dictionary

        Pre: the name of the station and a non negative x and y coordinate.
        """
        self.name: str = name
        self.x: float = x
        self.y: float = y

        self.connections: set[Station] = set()
        self.connections_durations: dict[Station, float] = {}

    def add_connection(self, station, duration: int) -> None:
        """
        Adds a connection to another station with a given duration.

        Pre: the station object that is connected to the main station
             and a duration that is a non negative number
        Post: filled up connections set with connected stations
              filled up connections_duration dictionary, with as key a station
              and the value the duration 
        """
        self.connections.add(station)
        self.connections_durations[station] = duration

    def has_connection(self, station) -> bool:
        """
        Checks if this station has a connection to another station.

        Pre: station object
        Post: True or False depending if the station is connected or not 
        """
        return station in self.connections

    def get_duration(self, station) -> Any:
        """
        Gets the duration of the connection to another station.

        Pre: station object
        Post: returns the time of the connections to the other station
              or it returns none 
        """
        if station and self.connections_durations.get(station):
            return self.connections_durations[station]
        else:
            return None
