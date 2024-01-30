import csv
from itertools import product
from random import randint, choices
from railnl import RailNL
from aco import Ant, ACO
import time
from typing import List, Tuple

def run_aco_and_write_to_csv(parameter_set: List[Tuple[int, float, float, int, int, int]], num_runs: int = 10) -> None:
    """
    Runs the ACO algorithm with the given parameter set and writes the results to a CSV file.
    Pre: parameter_set is a list of tuples containing the parameter values to be tested.
    Post: a CSV file is created containing the results of the ACO algorithm for each parameter combination.
    """
    total_combinations = len(parameter_set)
    current_combination = 0
    
    with open('results.csv', 'w', newline='') as csvfile:
        fieldnames = ['evaporation_rate', 'exploration_parameter', 'end_random_iterations', 'min_trajecten', 'max_trajecten', 'best_score', 'best_iteration', 'avg_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for params in parameter_set:
            current_combination += 1
            num_iterations, evaporation_rate, exploration_parameter, min_trajecten, max_trajecten, end_random_iterations = params
            best_results = {'best_score': 0, 'best_iteration': 0, 'avg_score': 0}

            for run in range(num_runs):
                print(f"Combination {current_combination}/{total_combinations}, Run {run + 1}/{num_runs}")

                best_score, best_iteration, avg_score = run_aco_with_time_limit(
                    num_iterations, evaporation_rate, exploration_parameter, min_trajecten, max_trajecten, end_random_iterations
                )

                if best_score > best_results['best_score']:
                    best_results['best_score'] = best_score
                    best_results['best_iteration'] = best_iteration
                    best_results['avg_score'] = avg_score

            writer.writerow({
                'evaporation_rate': evaporation_rate,
                'exploration_parameter': exploration_parameter,
                'end_random_iterations': end_random_iterations,
                'min_trajecten': min_trajecten,
                'max_trajecten': max_trajecten,
                'best_score': best_results['best_score'],
                'best_iteration': best_results['best_iteration'],
                'avg_score': best_results['avg_score']
            })

def run_aco_with_time_limit(num_iterations: int, evaporation_rate: float, exploration_parameter: float,
                            min_trajecten: int, max_trajecten: int, end_random_iterations: int) -> Tuple[float, int, float]:
    """
    Runs the ACO algorithm with the given parameters and a time limit of 3 minutes per iteration.
    Pre: num_iterations is an integer, evaporation_rate is a float, exploration_parameter is a float,
    min_trajecten is an integer, max_trajecten is an integer, end_random_iterations is an integer.
    Post: the best score, best iteration and average score of the ACO algorithm are returned.
    """
    rail_network = RailNL()
    aco = ACO()
    rail_network.load_stations('StationsNationaal.csv')
    rail_network.load_connections('ConnectiesNationaal.csv')
    aco.set_pheromones('ConnectiesNationaal.csv')
    best_score: int = 0
    best_netwerk: dict = None
    best_duration: int = 0
    list_scores: list = []
    best_scores_num_traject: dict = {}
    best_score_not_changed: int = 0
    threshold: int = 10000
    time_limit: int = 180
    calculations_done: bool = False
    for i in range(1, 21):
        best_scores_num_traject[i] = 0

    start_time = time.time()
    
    for i in range(num_iterations):
        if i < end_random_iterations:
            num_ants = randint(min_trajecten, max_trajecten)
        else:
            if not calculations_done:
                sum_scores = sum(best_scores_num_traject.values())
                weights = [score / sum_scores for score in best_scores_num_traject.values()]
                calculations_done = True
            num_ants = choices(list(best_scores_num_traject.keys()), weights=weights)[0]    
        ants = aco.deploy_ants(rail_network, num_ants)
        aco.totaal_trajecten.clear()

        for ant in ants:
            while ant.current_station is not None:
                ant.current_station = aco.choose_next_station(ant, 180, exploration_parameter)
                if ant.current_station is not None:
                    ant.traject.append(ant.current_station)
                    aco.update_unique_connections((ant.traject[-2].name, ant.traject[-1].name))

            aco.update_pheromones(rail_network, evaporation_rate)
            aco.totaal_trajecten[ant] = ant.traject
        exploration_parameter = max(0.1, exploration_parameter * 0.9999)
        list_scores.append(aco.total_score(rail_network))
        avg_score = sum(list_scores) / len(list_scores)
        
        score_totaal = aco.total_score(rail_network)
        if score_totaal > best_score:
            prev_best_score = best_score
            best_score = score_totaal
            best_netwerk = aco.totaal_trajecten
            best_duration = aco.duration_totaal
            best_iteration = i + 1
            best_score_not_changed = 0
        elif i > end_random_iterations:
            best_score_not_changed += 1
        if best_score_not_changed > threshold or best_score - prev_best_score < 10:
            print("Best score not changed for 10000 iterations")
            break
         
        if score_totaal > best_scores_num_traject[len(aco.totaal_trajecten)]:
            best_scores_num_traject[len(aco.totaal_trajecten)] = score_totaal
        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            print("Time limit reached")
            break
        
    return best_score, best_iteration, avg_score

if __name__ == '__main__':
    parameter_values = {
        'num_iterations': [50000],
        'evaporation_rate': [0.001, 0.005],
        'exploration_parameter': [0.3, 0.5, 0.7],
        'min_trajecten': [3],
        'max_trajecten': [18],
        'end_random_iterations': [500,1000],
    }
    parameter_set = list(product(*parameter_values.values()))
    
    run_aco_and_write_to_csv(parameter_set)
