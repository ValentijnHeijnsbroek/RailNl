import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Algorithms.greedy import *

greedy = greedy_algorithm(100)
greedy.print_output()
