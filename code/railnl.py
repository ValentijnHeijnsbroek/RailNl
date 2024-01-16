from station import Station
from traject import Traject
from connections import Connections
import numpy as np
import csv
import os
import matplotlib.pyplot as plt

class RailNL():
    def __init__(self):
        self.stations = []
        self.stations_connections = {}
        self.amount_of_connections = 0
        self.score = 10
        self.trajecten = {}

    def load_stations(self, station_filename):
        """
        loads stations into 2 different lists one for the name and 
        the other into a list of station variables
        The station names also get saved inside of a dictionary connected to an empty list

        """
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
        """
        loads the connections between stations and puts a station's connections with
        each station it has inside of a list.
        It also adds the distance between the connected station as a float with the
        2 stations being the key for that
        
        """
        with open(connection_filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                station_data = row[0]
                connection_data = row[1]
                duration_data = float(row[2])


                starting_connection = None
                ending_connection = None
                for station in self.stations:
                    if station.name == station_data:
                        starting_connection = station
                        
                        
                        # name_1 = station_data

                    if station.name == connection_data:
                        ending_connection = station
            
                if starting_connection and ending_connection:
                    starting_connection.add_connection(ending_connection, duration_data)
                    ending_connection.add_connection(starting_connection, duration_data)
                    self.amount_of_connections += 1
                    
        # using the name of the station to get the station variable 
    def get_station_by_name(self, station_name):
        for station in self.stations:
            if station.name == station_name:
                return station
        return None
    
    def plot_network(self):
        plt.figure(figsize=(8, 8))
        
        # Plot stations
        for station in self.stations:
            plt.scatter(station.x, station.y, marker='o', color='blue')

        # Plot connections
        for station in self.stations:
            for connected_station in station.connections.items():
                plt.plot([station.x, connected_station.x], [station.y, connected_station.y], color='gray', linestyle='solid')
        plt.title('Rail Network')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(False)
        plt.show()

    # Calculates and returns score.
    def get_score(self):
        """
        Calculates the K score as defined on the case website, returns an integer
        """
        sum_min = 0 # Min het aantal minuten in alle trajecten samen.
        bereden_trajecten = 0
        bereden_unique_station = set([])
        

        for traject_index in self.trajecten:
            sum_min += self.sum_time(traject_index)  # Berekent per traject de duration
            bereden_trajecten += len(self.trajecten[traject_index].traject_stations)   # Bekijkt per traject  hoeveel verbindingen er worden gelezen (Dit zorgt er alleen nog voor dat verbindingen dubbelgeteld kunnen worden)
        
            bereden_unique_station.update(self.trajecten[traject_index].traject_stations)
        
        if self.amount_of_connections == 0:
        # If there are no connections, return 0 for genetic algorithm
            return 0
        p =  len(bereden_unique_station) / self.amount_of_connections  # de fractie van de bereden verbindingen (dus tussen 0 en 1)
        T = len(self.trajecten) #het aantal trajecten
        K = p*10000 - (T*100 + sum_min)
        return round(K, 2)
    
    def create_traject(self, traject_index):
        """
        Create a empty traject
        """
        traject = Traject()
        # append the traject into the trajecten list
        self.trajecten[traject_index] = traject
        
        return traject
    
    def sum_time(self, traject_index):
        
        duration = 0

        for i in range(len(self.trajecten[traject_index].traject_stations) - 1):
            station1 = self.trajecten[traject_index].traject_stations[i]
            station2 = self.trajecten[traject_index].traject_stations[i + 1]

            if station1.connections_durations[station2]:
                duration += station1.connections_durations[station2]
                # print(duration)
        return duration

    # Saves output to csv file.
    def upload_output(self, output_filename):
        with open(output_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['train', 'stations'])
            for i in range(1, len(self.trajecten) + 1): 
                train_name = f'train_{i}'
                stations_list = [station.name for station in self.trajecten[i].traject_stations]
                writer.writerow([train_name, str(stations_list)])
            writer.writerow((['score', self.get_score()]))
    
    # Prints example output
    def print_output(self):
        for j in range(1, len(self.trajecten) +1 ):
            print(f"Traject: {j}")
            for i in range(len(self.trajecten[j].traject_stations)):
                print(self.trajecten[j].traject_stations[i].name)
            print(f"Duration for traject {j}: {self.sum_time(j)}")
            print(" ")
        print(f"Score: {self.get_score()}")
    
    # Method that clears all the trajects of the railnl instance.
    def clear_trajecten(self):
        self.trajecten = {}

    # Method that encodes solution to binary, using it as a experiment for genetic algorithm (Vaal)    
    def encode_solution(self):
        # Encode selected stations and connections as binary
        encoded_solution = []

        # Iterate over trajecten
        for traject_index in range(1, self.max_trajecten + 1):
            # Create a set of selected stations for each traject
            selected_stations = set(station for station in self.trajecten[traject_index].traject_stations)

            # Encode stations as binary (1 if selected, 0 if not)
            for station in self.stations:
                if station in selected_stations:
                    encoded_solution.append(1)
                else:
                    encoded_solution.append(0)

                # Encode the number of connections for each station
                encoded_solution.append(len(station.connections))

        return np.array(encoded_solution)

    
    def get_num_connections(self):
        return self.amount_of_connections
    
    # Werkt niet,, ben dit nu aan t proberen voor genetic algorithm
    def convert_solution(self, encoded_solution, rail_instance=None, threshold=0.5):
        if rail_instance is None:
            rail_instance = RailNL()

        traject_index = 1
        current_station = None

        # Decode stations and connections
        for index, value in enumerate(encoded_solution):
            # Check if the station is selected
            if value > threshold:
                station_index = index // 2
                if station_index < len(self.stations):
                    station = self.stations[station_index]

                    # Check if the station needs to be added to the current traject
                    if traject_index not in rail_instance.trajecten:
                        rail_instance.create_traject(traject_index)

                    rail_instance.trajecten[traject_index].add_station_to_traject(station)

                    # Update the current station
                    current_station = station

            # Check if a connection should be established
            if index % 2 == 1 and current_station is not None:
                connection_index = index // 2
                if connection_index < self.amount_of_connections:
                    connection_duration = 5
                    # Assuming your connections are stored as pairs of stations
                    other_station = self.stations[connection_index]
                    current_station.add_connection(other_station, connection_duration)

        return rail_instance








# Get the current directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))
# Navigate up one level to the parent directory
parent_directory = os.path.abspath(os.path.join(script_directory, '..'))
# Navigate to the directory where your data is located
data_directory = os.path.join(parent_directory, 'data')  # Change 'data' to the actual name of your data directory
# Set the working directory to the data directory
os.chdir(data_directory)

if __name__ == '__main__':
    NoordHolland = RailNL()
    NoordHolland.load_stations('StationsHolland.csv')
    NoordHolland.load_connections('ConnectiesHolland.csv')

    NoordHolland.create_traject(1)
    Amsterdam_Centraal = NoordHolland.get_station_by_name('Amsterdam Centraal')
    Amsterdam_Sloterdijk = NoordHolland.get_station_by_name('Amsterdam Sloterdijk')
    NoordHolland.trajecten[1].add_station_to_traject(Amsterdam_Centraal)
    NoordHolland.trajecten[1].add_station_to_traject(Amsterdam_Sloterdijk)
    print(NoordHolland.trajecten[1].traject_stations)
    NoordHolland.trajecten[1].delete_station(Amsterdam_Sloterdijk)
    print(NoordHolland.trajecten[1].traject_stations)

    #     assert rail_nl_instance.trajecten[1] == new_traject
    # # assert rail_nl_instance.trajecten[1].traject_stations[0] == Amsterdam_Centraal
    # # assert rail_nl_instance.trajecten[1].traject_stations[1] == Amsterdam_Sloterdijk

    # NoordHolland.create_traject()
    # print(NoordHolland.trajecten[0])
    # first = NoordHolland.trajecten[0]
    # Alkmaar = NoordHolland.stations[0]
    # first.add_station_to_traject(Alkmaar)
    # Hoorn = NoordHolland.get_station_by_name("Hoorn")
    # first.add_station_to_traject(Hoorn)
    # print(Hoorn.connections_durations)
    # Delft = NoordHolland.get_station_by_name("Delft")
    # first.add_station_to_traject(Delft)
    # print(first.traject_stations)
    # print(first.traject_stations)
