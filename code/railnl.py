from station import Station
from traject import Traject
import csv
import os
import matplotlib.pyplot as plt

class RailNL():
    def __init__(self):
        self.stations = []
        self.score = 10
        self.trajecten = []

    def load_stations(self, station_filename):
        with open(station_filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip the header row if it exists
            for row in reader:
                name = row[0]
                y = float(row[1])
                x = float(row[2])
                station = Station(name, x, y)
                self.stations.append(station)

    def load_connections(self, connection_filename):
        with open(connection_filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)

            for row in reader:
                station_data = row[0]
                connection_data = row[1]
                duration_data = float(row[2])

                connected_stations = []
                connected_stations.append((row[0], row[1]))

                for station in self.stations:
                    if station.name == station_data:
                        starting_connection = station
                    if station.name == connection_data:
                        ending_connection = station
                
                starting_connection.connections[ending_connection] = duration_data
                ending_connection.connections[starting_connection] = duration_data

    def plot_network(self):
        plt.figure(figsize=(8, 8))
        
        # Plot stations
        for station in self.stations:
            plt.scatter(station.x, station.y, marker='o', color='blue')

        # Plot connections
        for station in self.stations:
            for connected_station, duration in station.connections.items():
                plt.plot([station.x, connected_station.x], [station.y, connected_station.y], color='gray', linestyle='solid')
        plt.title('Rail Network')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(False)
        plt.show()


    # Calculates and returns score.
    def get_score(self):
        sum_min = 0 # Min het aantal minuten in alle trajecten samen.
        p = 0 # de fractie van de bereden verbindingen (dus tussen 0 en 1)
        T = 0 #het aantal trajecten
        K = p*10000 - (T*100 + sum_min)
        return K
    
    # Prints example output
    def print_output(self, output_filename):
        with open(output_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['train', 'stations'])
            for i in range(1, 4): 
                train_name = f'train_{i}'
                stations_list = [station.name for station in self.stations]
                writer.writerow([train_name, str(stations_list)])
            writer.writerow((['score', self.score]))
    
    # Creates a new traject
    def create_traject(self):
        traject = Traject()
        self.trajecten.append(traject)

    # Adds station object to existing traject
    def add_station_to_traject(self, station, traject_index):
        if len(self.trajecten[traject_index].stations) == 0:
            self.trajecten[traject_index].add_station(station)
            print("first station added to traject")

        # Checks if traject index is in range, and if the station has a connection with the station in the traject
        elif traject_index < len(self.trajecten) and self.trajecten[traject_index].stations[-1].has_connection(station):
            print("Has connection and in index")
            traject = self.trajecten[traject_index]
            traject.add_station(station)

        else:
            print("Error")


# Get the current directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))
# Navigate up one level to the parent directory
parent_directory = os.path.abspath(os.path.join(script_directory, '..'))
# Navigate to the directory where your data is located
data_directory = os.path.join(parent_directory, 'data')  # Change 'data' to the actual name of your data directory
# Set the working directory to the data directory
os.chdir(data_directory)

test = RailNL()
test.load_stations('StationsHolland.csv')
test.load_connections('ConnectiesHolland.csv')
# test.plot_network()
test.print_output("outputtest.csv")
test.create_traject()

alkmaar = test.stations[0]
random = test.stations[10]

test.add_station_to_traject(alkmaar, 0)
test.add_station_to_traject(random, 0)
print(test.trajecten[0].calculate_duration())