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

def plot_combined_boxplot(scores_list: List[float], labels: List[str], colors: List[str]):
    """
    gets the score list, the labels for each one and the colors and puts them
    into a combined boxplot, so that comparison is possible

    pre: scores_list, labels, colors
    post: a plot where a boxplot is shown for each algorithm
    """
    boxplots = plt.boxplot(scores_list, labels=labels, patch_artist=True)
    
    for patch, color in zip(boxplots['boxes'], colors):
        patch.set_facecolor(color)

    plt.xlabel('Algorithms')
    plt.ylabel('Scores')
    plt.title('Comparison of Algorithm Scores')
    plt.grid(True)
    plt.savefig('../data/pics/boxplot')

# Add the scores inside each of the representavily list
depth_first_scores = read_scores('/Users/mozouh/Desktop/SIUUU/RailNl/data/scores/depth_first_scores.txt')
aco_scores = read_scores('/Users/mozouh/Desktop/SIUUU/RailNl/data/scores/aco_scores.txt')
sim_annealing_scores = read_scores('/Users/mozouh/Desktop/SIUUU/RailNl/data/scores/simulated_annealing_scores.txt')
random_scores = read_scores('/Users/mozouh/Desktop/SIUUU/RailNl/data/scores/random_scores.txt')
greedy_scores = read_scores('/Users/mozouh/Desktop/SIUUU/RailNl/data/scores/greedy_scores.txt')

# The colors to distinguish each boxplot from another
colors = ["blue", "green", "red", "lime", "purple"]  

# Call the function
plot_combined_boxplot(
    [depth_first_scores, aco_scores, sim_annealing_scores, random_scores, greedy_scores],
    ["Depth First", "ACO", "Sim Annealing", "Random", "Greedy"],
    colors
)
