from station import Station
from traject import Traject
from matplotlib.widgets import CheckButtons
from typing import Any, Optional

import mplcursors
import geopandas as gpd
import csv
import os
import matplotlib.pyplot as plt
from typing import list, Tuple, Set

class RailNL():
    def __init__(self):
        self.stations: List = []
        self.stations_connections: dict = {}
        self.amount_of_connections: int = 0
        self.score: int = 10
        self.trajecten: dict = {}

        # For visualization purposes
        self.iterations_list: List = []
        self.scores_list: List = []


    def load_stations(self, station_filename: str) -> None:
        """
        loads stations into 2 different lists one for the name and 
        the other into a list of station variables
        The station names also get saved inside of a dictionary connected to an empty list

        pre: station_filename string
        post: the station objects gets loaded inside of the self.stations list
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

    def load_connections(self, connection_filename: str) -> None:
        """
        loads the connections between stations and puts a station's connections with
        each station it has inside of a list.
        it also adds the distance between the connected station as a float with the
        2 stations being the key for that

        pre: connection_filename string
        post: station connection formed 
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
                        

                    if station.name == connection_data:
                        ending_connection = station
            
                if starting_connection and ending_connection:
                    starting_connection.add_connection(ending_connection, duration_data)
                    ending_connection.add_connection(starting_connection, duration_data)
                    self.amount_of_connections += 1
                    
        # using the name of the station to get the station variable 
    def get_station_by_name(self, station_name: str) -> Any:
        """
        uses the name of a station to give the station object

        pre: station_name string
        post: the station object or None depending if the station object with the station name exists 
        """
        for station in self.stations:
            if station.name == station_name:
                return station
        return None

    
    def plot_network(self) -> None:
        """
        creates a plot showing the trajects with different lines and it also shows
        the station with their corresponding name when hovering over it.
        The user can also pick which trajects are shown or not using the checkboxes.

        post: A plot with the Netherlands as background, the trajects shown with lines, and the 
            stations are shown as points.
        """
        # Read GeoJSON file for background
        background_geojson_path = '../data/nl_regions.geojson'
        background_data = gpd.read_file(background_geojson_path)

        # Plot background
        fig, ax = plt.subplots(figsize=(8, 8))
        background_data.plot(ax=ax, color='lightgray')

        # Plot connections from trajecten
        line_styles = ['-', '--', '-.', ':']
        traject_lines = []  # Keep track of lines associated with each traject
        traject_labels = []  # Keep track of unique traject labels for legend
        for traject_index in self.trajecten:
            traject_stations = self.trajecten[traject_index].traject_stations
            colorr = plt.cm.rainbow(traject_index / len(self.trajecten))
            style_index = traject_index % len(line_styles)
            style = line_styles[style_index]

            lines = []
            for i in range(len(traject_stations) - 1):
                station1 = traject_stations[i]
                station2 = traject_stations[i + 1]
                
                # So that the lines are not on top of each other
                offset = 0.01 * (i % 2)

                line, = ax.plot([station1.x, station2.x], [station1.y + offset, station2.y + offset],
                        color=colorr, linestyle=style, linewidth=2, alpha=0.9, label=f'Traject {traject_index}')
                lines.append(line)

            traject_lines.append(lines)
            traject_labels.append(f'Traject {traject_index}')


        # Plot stations with explicit labels
        for station in self.stations:
            scatter_point = plt.scatter(station.x, station.y, marker='o', color='blue')
            scatter_point.set_label(station.name)  # Set the label for the scatter point

        plt.title('Rail Network Netherlands')

        # Set axis limits based on the range of station coordinates
        min_x = min(station.x for station in self.stations) 
        max_x = max(station.x for station in self.stations) 
        min_y = min(station.y for station in self.stations) 
        max_y = max(station.y for station in self.stations)

        # Add some padding to the limits
        padding = 0.4
        ax.set_xlim(min_x - padding, max_x + padding)
        ax.set_ylim(min_y - padding, max_y + padding)

        ax.axis('off')
        plt.grid(False)

        # Use mplcursors to capture mouse events and show station names on hover
        cursor = mplcursors.cursor(hover=True)

        # Handles hover events to show station names
        def on_hover(sel):
            x, y = sel.target
            station = self.get_station_by_coordinates(x, y)
            if station is not None:
                label = station.name
                sel.annotation.set_text(label)
                sel.annotation.set_visible(True)  # laat de stationnaam zien
            else:
                sel.annotation.set_visible(False)

        cursor.connect("add", on_hover)

        # Create checkboxes for trajects
        traject_labels = [f'Traject {i}' for i in self.trajecten]
        traject_checkboxes = CheckButtons(plt.axes([0.01, 0.01, 0.2, 0.2]),
                                        traject_labels,
                                        [True] * len(self.trajecten))

        # Get handles and labels for lines (excluding scatter plot handles)
        line_handles, line_labels = [], []
        for lines, label in zip(traject_lines, traject_labels):
            line_handles.append(lines[0])  # Only add the first line of each trajectory to the legend
            line_labels.append(label)

        # Handles checkbox clicks to toggle visibility of trajectories
        def update_visibility(label):
            traject_index = int(label.split()[-1])  # Extract traject index from label

            # Toggle visibility of traject lines
            visibility = not all(line.get_visible() for line in traject_lines[traject_index - 1])
            for line in traject_lines[traject_index - 1]:
                line.set_visible(visibility)

            # Update legend handles and labels
            updated_line_handles = []
            updated_line_labels = []
            for line, lbl in zip(line_handles, line_labels):
                if line.get_visible():
                    updated_line_handles.append(line)
                    updated_line_labels.append(lbl)

            # Remove the existing legend
            plt.gca().get_legend().remove()

            # Explicitly add a new legend outside the checkboxes
            plt.legend(handles=updated_line_handles, labels=updated_line_labels, loc='upper right', bbox_to_anchor=(4.8, 3.8))
            plt.draw()
        traject_checkboxes.on_clicked(update_visibility)

        # Move the legend to the upper right
        plt.legend(handles=line_handles, labels=line_labels, loc='upper right', bbox_to_anchor=(4.8, 3.8))

        plt.show()
    
    
    def get_station_by_coordinates(self, x: float, y: float) -> Optional[Station]:
        """
        uses the coordinates to get the station object connected to it

        pre: x and y floats 
        post: return the station object or None, depending on if the station object exist or not
        """
        epsilon: float = 0.01
        for station in self.stations:
            if abs(station.x - x) < epsilon and abs(station.y - y) < epsilon:
                return station
        return None


    # Calculates and returns score.
    def get_score(self) -> float:
        """
        calculates the K score as defined on the case website, returns an integer
        
        post: calculates the score based on:
              p: what perecentage of all the connections are covered
              T: the amount of trajects inside of the RailNL
              sum_min: de total time of all the trajects
        """
        sum_min = 0 # Min het aantal minuten in alle trajecten samen.
        bereden_trajecten: int = 0
        bereden_unique_verbinding: set[List]= set([])
        T = len(self.trajecten) #het aantal trajecten
        for traject_index in self.trajecten:
            sum_min += self.sum_time(traject_index)  # Berekent per traject de duration
            bereden_trajecten += len(self.trajecten[traject_index].traject_stations)   # Bekijkt per traject  hoeveel verbindingen er worden gelezen
            #(Dit zorgt er alleen nog voor dat verbindingen dubbelgeteld kunnen worden)
            # If traject is empty, it does not get counted.
            for i in range(len(self.trajecten[traject_index].traject_stations) - 1):
                station1 = self.trajecten[traject_index].traject_stations[i]
                station2 = self.trajecten[traject_index].traject_stations[i + 1]
                tuple1 = (station1.name, station2.name)
                tuple2 = (station2.name, station1.name)
                bereden_unique_verbinding.add(tuple1)
                bereden_unique_verbinding.add(tuple2)
        
        if self.amount_of_connections == 0:
        # If there are no connections, return 0 for genetic algorithm
            return 0
        p: float =  (len(bereden_unique_verbinding)/2) / self.amount_of_connections  # de fractie van de bereden verbindingen (dus tussen 0 en 1)
        
        K: float= p*10000 - (T*100 + sum_min)
        
        return round(K, 2)
    
    def create_traject(self, traject_index) -> Traject:
        """
        creates a new empty traject and adds a traject_index to it

        pre: traject index integer
        post: an empty traject with a traject_index connected to it inside the dictionary
        """
        traject: 'Traject' = Traject()
    
        # append the traject into the trajecten list
        self.trajecten[traject_index] = traject
        
        return traject
    
    def sum_time(self, traject_index: int) -> int:
        """
        calculates the sum time of the traject

        pre: traject index 
        post: the total duration of the traject 
        """
        
        duration: int = 0

        # Gets the duration for each connection in the traject
        for i in range(len(self.trajecten[traject_index].traject_stations) - 1):
            station1 = self.trajecten[traject_index].traject_stations[i]
            station2 = self.trajecten[traject_index].traject_stations[i + 1]

            # Add it to the duration sum
            if station1.connections_durations[station2]:
                duration += station1.connections_durations[station2]
        return duration

    # Saves output to csv file.
    def upload_output(self, output_filename) -> csv:
        """
        uploads the output inside the file_name 

        pre: the outputname of the file name which is a string
        post: file gets created with the output and score
        """
        with open(output_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['train', 'stations'])
            for i in range(1, len(self.trajecten) + 1): 
                train_name = f'train_{i}'
                stations_list = [station.name for station in self.trajecten[i].traject_stations]
                writer.writerow([train_name, str(stations_list)])
            writer.writerow((['score', self.get_score()]))
    
    # Prints example output
    def print_output(self) -> str:
        """
        prints out the example output with the score and the total time for each traject

        post: output gets printed inside the terminal
        """
        for j in range(1, len(self.trajecten) +1 ):
            if self.trajecten[j].traject_stations == []:
                continue
            else:
                print(f"Traject: {j}")
                for i in range(len(self.trajecten[j].traject_stations)):
                    print(self.trajecten[j].traject_stations[i].name)
                print(f"Duration for traject {j}: {self.sum_time(j)}")
                print(" ")
        print(f"Score: {self.get_score()}")
    
    # Method that clears all the trajects of the railnl instance.
    def clear_trajecten(self) -> None:
        """
        gets rid of all trajects inside the railnl

        post: self.trajecten gets emptied
        """
        self.trajecten = {}


    def get_num_connections(self) -> int:
        """
        looks at how many total connections there are from the connections file 

        post: self.amount_of_connections
        """
        return self.amount_of_connections

        # Delete traject, and adjusts every traject index so that it is numbered from 1 to len(trajecten)
    def delete_traject(self, traject_index: int) -> None:
        """
        deletes a specific traject when a traject_index is given

        pre: traject_index integer
        post: the specific traject gets deleted 
        """
        if traject_index in self.trajecten:
            del self.trajecten[traject_index]
            for i in range(traject_index, len(self.trajecten) + 1):
                self.trajecten[i+1] = i
        else:
            print(f"ERROR: Traject {traject_index} does not exist.")


# Get the current directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))
# Navigate up one level to the parent directory
parent_directory = os.path.abspath(os.path.join(script_directory, '..'))
# Navigate to the directory where your data is located
data_directory = os.path.join(parent_directory, 'data')  # Change 'data' to the actual name of your data directory
# Set the working directory to the data directory
os.chdir(data_directory)

