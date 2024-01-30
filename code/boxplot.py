import matplotlib.pyplot as plt
import os

def read_scores(file_path):
    with open(file_path, 'r') as file:
        return [float(line.strip()) for line in file]

def plot_combined_boxplot(scores_list, labels, colors):
    boxplots = plt.boxplot(scores_list, labels=labels, patch_artist=True)
    
    for patch, color in zip(boxplots['boxes'], colors):
        patch.set_facecolor(color)

    plt.xlabel('Algorithms')
    plt.ylabel('Scores')
    plt.title('Comparison of Algorithm Scores')
    plt.grid(True)
    plt.show()

# Example usage
print("Current working directory:", os.getcwd())
depth_first_scores = read_scores('/Users/mozouh/Desktop/SIUUU/RailNl/data/depth_first_scores.txt')
aco_scores = read_scores('/Users/mozouh/Desktop/SIUUU/RailNl/data/aco_scores.txt')
hill_climber_scores = read_scores('/Users/mozouh/Desktop/SIUUU/RailNl/data/simulated_annealing_scores.txt')

colors = ["blue", "green", "red"]  # Specify your colors here
plot_combined_boxplot(
    [depth_first_scores, aco_scores, hill_climber_scores],
    ["Depth First", "ACO", "Simulated Annealing"],
    colors
)
