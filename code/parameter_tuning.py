import csv
from itertools import product
from random import randint, choices
from railnl import RailNL
from aco import Ant, ACO
import time

def run_aco_and_write_to_csv(parameter_set):
    with open('results.csv', 'w', newline='') as csvfile:
        fieldnames = ['evaporation_rate', 'exploration_parameter', 'end_random_iterations', 'min_trajecten', 'max_trajecten', 'best_score', 'best_iteration', 'avg_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for params in parameter_set:
            num_iterations, evaporation_rate, exploration_parameter, min_trajecten, max_trajecten, end_random_iterations = params
            best_score, best_iteration, avg_score = run_aco_with_time_limit(num_iterations, evaporation_rate, exploration_parameter, min_trajecten, max_trajecten, end_random_iterations)
            
            writer.writerow({
                'evaporation_rate': evaporation_rate,
                'exploration_parameter': exploration_parameter,
                'end_random_iterations': end_random_iterations,
                'min_trajecten': min_trajecten,
                'max_trajecten': max_trajecten,
                'best_score': best_score,
                'best_iteration': best_iteration,
                'avg_score': avg_score
            })
            print("Parameters:", params, "Results:", best_score, best_iteration, avg_score)

def run_aco_with_time_limit(num_iterations, evaporation_rate, exploration_parameter, min_trajecten, max_trajecten, end_random_iterations):
    rail_network = RailNL()
    aco = ACO()
    rail_network.load_stations('StationsNationaal.csv')
    rail_network.load_connections('ConnectiesNationaal.csv')
    aco.set_pheromones('ConnectiesNationaal.csv')
    best_score = 0
    best_netwerk = None
    best_duration = 0
    list_scores = []
    best_scores_num_traject = {}
    best_score_not_changed = 0
    threshold = 10000
    time_limit = 180
    calculations_done = False
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
        'evaporation_rate': [0.001, 0.005, 0.01, 0.05],
        'exploration_parameter': [0.3, 0.5, 0.7],
        'min_trajecten': [3, 5],
        'max_trajecten': [18, 20],
        'end_random_iterations': [500, 1000, 5000, 10000],
    }
    parameter_set = list(product(*parameter_values.values()))
    
    run_aco_and_write_to_csv(parameter_set)
