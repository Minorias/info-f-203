from algorithms import *
from itertools import chain

class Node:
    def __init__(self,name):
        self.name = name
        self.creditors = []
        self.debtors = []

    def add_creditor(self, creditor, amount):
        self.creditors.append([creditor, amount])

    def add_debtor(self,creditor):
        self.debtors.append(creditor)

    def get_all_related(self):
        return chain(self.get_creditors(), self.get_debtors())

    def get_creditors(self):
        """
        Returns only the objects of nodes to whom this nodes owes money
        """
        return map(lambda x: x[0], self.creditors)

    def get_debtors(self):
        """
        Returns the list of debtors.
        """
        return self.debtors

    def get_name(self):
        return self.name

    def get_creditor_amount(self, creditor):
        # Returns the amount that this person owes to a specified creditor
        return [cred for cred in self.creditors if cred[0] == creditor][0][1]

    def reduce_creditor_amount(self, creditor, new_amount):
        # This returns the list [creditor, amount] for the given creditor
        creditor = [cred for cred in self.creditors if cred[0] == creditor][0]

        # Due to the magic of list references, this will modify the original
        #   amount in the original list
        creditor[1] -= new_amount

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name


class Graph:
    def __init__(self, node_list):
        self.nodes = node_list

    def find_sccs(self):
        return SCCs_Tarjan(self.nodes, set()).find_sccs()

    def find_cycles(self):
        return Cycles_Johnson(self.nodes).get_cycles()

    def simplify_debts(self):
        cycles = Cycles_Johnson(self.nodes).get_cycles()

        # cycles[-1], cycles[-2] = cycles[-2], cycles[-1] Uncomment this to have same solution as assistant

        for cycle in cycles:
            # print(cycle)
            debt_to_simplify = infinity

            for i in range(len(cycle) - 1):
                current_node = cycle[i]
                next_node = cycle[i+1]
                debt_to_simplify = min(debt_to_simplify, current_node.get_creditor_amount(next_node))

            # print(debt_to_simplify)

            for i in range(len(cycle) - 1):
                current_node = cycle[i]
                next_node = cycle[i+1]

                current_node.reduce_creditor_amount(next_node, debt_to_simplify)

    def ouput_graph(self):
        for node in self.nodes:
            for creditor in node.get_creditors():
                print(node, creditor, node.get_creditor_amount(creditor))

    def find_communities(self):
        return Communities(self.nodes).find_communities()

class HubFinder:
    """
    Finds the articulation points dividing the graph in subgraphs
    of at least K nodes each.
    """
    def __init__(self,graph,K=2):
        self.communities = Communities(graph.nodes).find_communities()
        self.k = K
        self.hubs_list = []
        for community in self.communities:
            self.time_list = {node : 0 for node in community}
            self.lowest_time = {node : 0 for node in community}
            self.visited = {node : False for node in community}
            self.predecessors = {node : None for node in community}
            self.visited_time = 0

            for node in community:
                if not self.visited[node]:
                    self.get_hubs(community,node)
        
        self.dfs_visited = set()
        self.the_real_slim_hubslist = []

        self.check_kkk()
        print(self.the_real_slim_hubslist)
    

    def get_hubs(self,community,root):
        self.time_list[root] = self.visited_time #Set "time" of visit.
        self.lowest_time[root] = self.visited_time
        self.visited_time +=1
        successors =0
        self.visited[root] = True
        for adj in root.get_all_related():

            if not self.visited[adj]:
                self.predecessors[adj] = root
                successors+=1
                self.get_hubs(community,adj)
                self.lowest_time[root] = min(self.lowest_time[root],self.lowest_time[adj])

                #If treeroot and more than 1 child or not root and no child to ancestor link.
                if not self.predecessors[root] and successors > 1 or \
                 self.predecessors[root] and self.lowest_time[adj] >= self.time_list[root]:
                    
                    if root not in self.hubs_list: 
                        self.hubs_list.append(root)

            elif adj != self.predecessors[root]: #
                self.lowest_time[root] = min(self.lowest_time[root],self.time_list[adj])

    def check_kkk(self):
        for point in self.hubs_list:
            lengths = []
            for related in point.get_all_related():
                self.dfs_visited.add(point)
                self.deafmutemidget(related)
                lengths.append(len(self.dfs_visited) - 1)
                self.dfs_visited = set()

            if all(x >= self.k for x in lengths):
                self.the_real_slim_hubslist.append(point)



    def deafmutemidget(self, current_node):
        self.dfs_visited.add(current_node)
        for related in current_node.get_all_related():
            if related not in self.dfs_visited:
                self.deafmutemidget(related)



