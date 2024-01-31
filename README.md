# Readme


To the user
This repository is dedicated to optimizing the rail network between intercitystations in the netherlands. By optimizing we mean maximizing a so called score-function, which gives us an indication how good a certain solution to this problem really is. This is the formula of the score function: K = p * 10000 - (100 * T + min), where p is the fraction of connections between stations visited, T is the number of trajectories i.e. the number of different train routes, and min is sum of the durations of all the trajectories in minutes. If one wants to maximize this score function, it is essential to try creating a rail network that visits as many unique connections with as few trajectories as possible in as small an amount of time as possible. Furthermore, there is the restriction that an individual trajectory can never be longer than 180 minutes. We have tried to tackle this problem by experimenting with three diferent algorithms: simulated annealing, depth first and ant colony optimization. How these algorithms work and how results can be reproduced, is described below.
## Simulated Annealing

### Running Simulated Annealing:

Open the simulated_annealing.py file.
Adjust the parameters (e.g., initial_temperature, cooling_rate, etc.) within the code to suit your requirements.
Run the script to execute the simulated annealing algorithm with the specified parameters.
Review the output and any relevant files generated by the algorithm.



### Running parameter tuning:

open  the parameter_tuning_sim_annealing.py file.
Inside the function, set the desired values for initial_temperatures and cooling_rates.
Run the script to perform a grid search on the specified parameter combinations.
Examine the results, including the scores obtained for each parameter combination.
Identify the best parameter set based on the highest score.

## Depth first

### Running the Depth First Algorithm

To effectively run the depth first algorithm, follow these steps:

### Select the Map
1. Open `depth_first.py`.
2. Choose the map you wish to use for the algorithm. You can select either `Holland` or `Nationaal`.
3. Set the map by changing the value in the `initialize_rail('Holland'/'Nationaal')` function call accordingly.
4. Additionally, adjust the file path for the map data. Change the `Nationaal` part of the file path to `Holland` if you are using the Holland map.

### Configure Parameters
1. Open `parameter_test_depth_first.py`.
2. Modify the parameters according to your requirements like: max iterations, max attempts per rail, etc. These parameters will influence the behavior and output of the algorithm.

### Run the Algorithm
Run `parameter_test_depth_first.py`. This will execute the depth first algorithm with the specified parameters and map.

### Output
Upon completion, the algorithm provides:
- A **score** indicating the effectiveness of the generated routes.
- A **visual map** depicting the routes.
- A **PNG file** illustrating the progression of scores achieved by the algorithm.
- To start when inputting the parameter max_aantal_trajecten at 15 and the the minimum amount of stations
per traject at 3, it will give the score around the 6400/6500 the quickest and consistently 



## Ant Colony Optimization
Ant Colony Optimization (ACO) is inspired by how an ant colony finds the best routes to food: if an ants dicsovers a fast route, it will leave a trail of pheromones behind that other ants can smell. Stronger pheromone levels mean better or faster routes. In this manner, ants can very quickly find the best path to their food. In our code it works almost the same: each iteration a certain amount of 'ants' is deployed over stations. Each ant represents a possible trajectory. Beforehand a predetermined amount of pheromones is set to all connections. Each ant will choose his next station based on the pheromone levels of that connection that are left behind by ants in previous generations. At the end of each iteration the highest of the trajectories (ants) will be rewarded by giving all the connections in that trajectory some extra pheromones. 

To avoid pheromone levels getting too high, and thereby unstimulating the ants to explore not yet dicsovered connections, each iteration all connections are deducted a small amount of their pheromones(evaporation_rate). To further explore possible solutions, a parameter is specified(end_random_iterations) that controls when the number of ants are no longer randomly chosen, but chosen based on previous iterations. By correctly tuning the parameters, this algorithm can be used to optimise the score function. If for a certain amount of iterations(threshold) the algorithm doesn't yield a score that's at least 10 points higher than the previous highscore , the algorithm will stop.

### Choosing map size and parameters
1: Open the 'aco.py' file
2: Choose the map size by setting the network_size_stations and the network_size_connections variables. By default StationsNationaal.csv   en ConnectiesNationaal.csv
3: Set the other parameters to your liking

### Run the algorithm:
Run the algorithm by executing the aco.py file

### Output:
The output will appear in the terminal.
From left to right: percentage showing the progress made, average score so far, highest score so far and number of iterations without highest score changing. When the algorithm is finished it will output the highest score, the iteration in wchich the highest score was achieved and the trajectories of the highest score.

### Parameter tuning
Open the 'parameter_tuning_aco.py' file
Scroll all the way down to the defining of the parameter spaces in the parameter_values dictionary
Add for each key (parameter) in the dictionary the dicrete space you want to search by adding values to the list of that key or by changing the current values.
Also specify the amount of times you want to try each combination of parameters by setting num_runs. If num_runs is higher than 1, the highest score of the tries per combination will be saved.
The results will be uploaded to 'best_results.csv'


