from station import Station
from traject import Traject
from connections import Connections
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
            for connected_station, duration in station.connections.items():
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
            
        p =  len(bereden_unique_station) / self.amount_of_connections  # de fractie van de bereden verbindingen (dus tussen 0 en 1)
        T = len(self.trajecten) #het aantal trajecten
        K = p*10000 - (T*100 + sum_min)
        return K
    
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

    new_traject = NoordHolland.create_traject(0)
    Amsterdam_Centraal = NoordHolland.get_station_by_name('Amsterdam Centraal')
    Amsterdam_Amstel= NoordHolland.get_station_by_name('Amsterdam Amstel')
    new_traject.add_station_to_traject(Amsterdam_Centraal)
    new_traject.add_station_to_traject(Amsterdam_Amstel)
    print("test")
    print(Amsterdam_Amstel.connections)
    print(len(NoordHolland.trajecten[0].traject_stations))
    score = NoordHolland.get_score()
    print("testbereden")
    print(NoordHolland.trajecten[0].is_bereden(Amsterdam_Centraal))


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
