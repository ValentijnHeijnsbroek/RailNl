from station import Station
import csv
import matplotlib.pyplot as plt

class RailNL():
    def __init__(self):
        self.stations = []
        self.score = 10

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


    def get_score(self):
        sum_min = 0 # Min het aantal minuten in alle trajecten samen.
        p = 0 # de fractie van de bereden verbindingen (dus tussen 0 en 1)
        T = 0 #het aantal trajecten
        K = p*10000 - (T*100 + sum_min)
        return K
    
    def print_output(self, output_filename):
        with open(output_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['train', 'stations'])
            for i in range(1, 4):  # Assuming there are 3 trains as per your example
                train_name = f'train_{i}'
                stations_list = [station.name for station in self.stations]
                writer.writerow([train_name, str(stations_list)])
            writer.writerow((['score', self.score]))

test = RailNL()
test.load_stations('StationsHolland.csv')
test.load_connections('ConnectiesHolland.csv')
# test.plot_network()
test.print_output("outputtest.csv")
