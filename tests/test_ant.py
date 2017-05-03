import pickle
import sys,pdb
import numpy as np
sys.path.insert(0,'../')

from antcolony.antcolony import AntColony
from antcolony.antgraph import AntGraph
from solvepath import solve_tsp_mat,analyse_tsp_solutions

#default
num_nodes = 10
np.random.seed(7)

if __name__ == "__main__":   
    if len(sys.argv) > 1 and sys.argv[1]:
        num_nodes = int(sys.argv[1])

    stuff = pickle.load(open("citiesAndDistances.pickled", "r"))
    cities = stuff[0]
    cost_mat = stuff[1]

    cost_mat=np.array(cost_mat)[:num_nodes,:num_nodes]
    print cost_mat
    best_path_vec,best_path_cost=solve_tsp_mat(cost_mat)
    analyse_tsp_solutions(best_path_vec,best_path_cost)
