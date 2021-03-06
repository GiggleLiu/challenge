import numpy as np

class Ant(object):
    def __init__(self, start_node, graph,end_node=None,alpha=1,beta=1,prob_exploitation=0.5,rho=0.99):
        self.start_node = start_node
        self.end_node=end_node if end_node is not None else start_node
        self.graph = graph

        # same meaning as in standard equations
        self.alpha = alpha
        self.beta = beta
        self.prob_exploitation = prob_exploitation
        self.rho = 0.99
        self.xi=self.graph.delta_mat.mean()

        self.reset()

    def reset(self):
        # store the nodes remaining to be explored here
        self.path_vec = [self.start_node]

        self.nodes_to_visit = range(self.graph.num_nodes)
        self.nodes_to_visit.remove(self.start_node)
        if self.end_node!=self.start_node:
            self.nodes_to_visit.remove(self.end_node)

    def run(self):
        graph = self.graph
        curr_node=self.start_node
        num_unvisited=len(self.nodes_to_visit)+1
        for i in xrange(num_unvisited):
            if i!=num_unvisited-1:
                new_node=self.state_transition_rule(curr_node)
            else:
                new_node=self.end_node
            self.path_vec.append(new_node)

            #update pheromone locally
            self.update_pheronmone_local(curr_node,new_node)
            curr_node = new_node

    def update_pheronmone_local(self,curr_node,next_node):
        graph=self.graph
        graph.tau_mat[curr_node, next_node]=graph.tau_mat[curr_node, next_node]*(1-self.rho)+self.rho*graph.tau0

    def get_path_cost(self):
        return self.graph.delta_mat[self.path_vec[:-1],self.path_vec[1:]].sum()

    # described in report -- determines next node to visit after curr_node
    def state_transition_rule(self, curr_node):
        graph = self.graph
        nodes_to_visit=self.nodes_to_visit

        if np.random.random() < self.prob_exploitation:
            #val = graph.tau_mat[curr_node, nodes_to_visit]**self.alpha/graph.delta_mat[curr_node, nodes_to_visit]**self.beta
            val = graph.tau_mat[curr_node, nodes_to_visit]**self.alpha*np.exp(-graph.delta_mat[curr_node, nodes_to_visit]**self.beta/self.xi)
            inode=np.argmax(val)
        else:
            #p=graph.tau_mat[curr_node, nodes_to_visit]**self.alpha/graph.delta_mat[curr_node, nodes_to_visit]**self.beta
            p=graph.tau_mat[curr_node, nodes_to_visit]**self.alpha*np.exp(-graph.delta_mat[curr_node, nodes_to_visit]**self.beta/self.xi)
            p=p/p.sum()
            inode=np.searchsorted(np.cumsum(p),np.random.random())
        max_node=nodes_to_visit.pop(inode)
        return max_node
