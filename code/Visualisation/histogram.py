import matplotlib.pyplot as plt
import os
from typing import List

def read_scores(file_path: str):
    """
    reads the scores from the from each line

    pre: file path name
    post: a list filled with the scores
    """
    with open(file_path, 'r') as file:
        return [float(line.strip()) for line in file]

def plot_combined_histogram(scores_list: List[float], labels: List):
    """
    gets the score list, the labels for each one and puts them
    into a combined histogram, so that comparison is possible

    pre: scores_list, labels
    post: a plot where histograms are shown for each algorithm
    """
    for scores, label in zip(scores_list, labels):
        plt.hist(scores, bins=50, alpha=0.7, label=label)
    
    plt.xlabel('Scores')
    plt.ylabel('Frequency')
    plt.title('Comparison of Algorithm Scores')
    plt.legend()
    plt.grid(True)
    plt.show()

# Add the scores inside each of the representavily list
print("Current working directory:", os.getcwd())
depth_first_scores = read_scores('/Users/mozouh/Desktop/SIUUU/RailNl/data/depth_first_scores.txt')
aco_scores = read_scores('/Users/mozouh/Desktop/SIUUU/RailNl/data/aco_scores.txt')
sim_annealing_scores = read_scores('/Users/mozouh/Desktop/SIUUU/RailNl/data/simulated_annealing_scores.txt')
random_scores = read_scores('/Users/mozouh/Desktop/SIUUU/RailNl/data/random_scores.txt')
greedy_scores = read_scores('/Users/mozouh/Desktop/SIUUU/RailNl/data/greedy_scores.txt')

plot_combined_histogram(
    [depth_first_scores, aco_scores, sim_annealing_scores, random_scores, greedy_scores],
    ["Depth First", "ACO", "Sim Annealing", "Random", "Greedy"],
)
