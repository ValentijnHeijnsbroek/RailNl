import csv
class Station:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

        # self.connections = {}

    def has_connection(self, station):
        return station in self.connections
