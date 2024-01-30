import subprocess
import time
import csv
start = time.time()
n_runs = 0

# Open the CSV file for writing

with open('results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Run', 'Result'])  # Write header row

    while time.time() - start < 1200:
        print(f"run: {n_runs}")
        subprocess.call(["timeout", "90", "python3", "aco.py"])

        # Write the result to the CSV file
        writer.writerow([n_runs, best_score])  # Replace `result` with the actual result variable

        n_runs += 1
    
    n_runs += 1