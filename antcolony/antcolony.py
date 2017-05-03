import numpy as np
import sys,pdb

from ant import Ant

class AntColony:
    def __init__(self, graph, num_ants, start_node=0, end_node=None, Rho=0.1):
        self.graph = graph
        self.Rho = Rho
        self.num_ants=num_ants
        self.start_node=start_node
        self.end_node=end_node

        self.reset()

    def reset(self):
        self.best_path_cost = np.Inf
        self.best_path_vec = None

        self.ants = []
        for i in xrange(self.num_ants):
            ant = Ant(start_node=self.start_node,end_node=self.end_node,graph=self.graph)
            self.ants.append(ant)

    def run(self,num_iterations):
        self.reset()
        for i in xrange(num_iterations):
            path_costs=[]
            for ant in self.ants:
                ant.run()
                path_cost=ant.get_path_cost()
                path_costs.append(path_cost)
                if path_cost < self.best_path_cost:
                    self.best_path_cost = path_cost
                    self.best_path_vec = ant.path_vec
            avg_path_cost=np.mean(path_costs)
            for ant in self.ants:
                ant.reset()

            self.update_pheromone()
        print "Best: %s, %s, %s, %s" % (self.best_path_vec, self.best_path_cost, i, avg_path_cost,)

    def update_pheromone(self):
        '''Update Pheromone on the graph.'''
        pos=self.best_path_vec[:-1],self.best_path_vec[1:]
        self.graph.tau_mat*=(1-self.Rho)
        self.graph.tau_mat[pos]+=self.Rho/self.best_path_cost
