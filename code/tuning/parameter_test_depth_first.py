import sys
import os

# Adjust sys.path to include the directory of help_funtions.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Algorithms')))

from depth_first import * 

# the max amount of minutes a traject is allowed to have
max_aantal_minuten = 180

# the max amount of trajecten the rail is allowed to have
max_aantal_trajecten = 16

# max amount of visitation a station is allowed to have in the rail
threshold_visit_frequency = 8

# how many attempts to find better combinations for the rail
max_attempts = 550

# minimum stations per traject
min_stations = 3

# how deep it looks through each traject 
max_depth = 75

#amount of rail getting made
iterations = 1200

# the amount of secondes the code will run
max_time = 1200

# if score hasent improved, central hubs list resets
no_improvement_threshold = 20

best_rail = iterative_depth_first(max_depth, iterations, central_hubs, no_improvement_threshold, max_aantal_minuten, max_aantal_trajecten, threshold_visit_frequency, max_attempts, min_stations, max_time)

best_rail.print_output()
best_rail.upload_output('depth_first_search.csv')
best_rail.plot_network()
