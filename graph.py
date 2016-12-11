from itertools import chain
from math import inf as infinity

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

    def change_creditor_amount(self, creditor, new_amount):
        # This returns the list [creditor, amount] for the given creditor
        creditor = [cred for cred in self.creditors if cred == creditor][0]

        # Due to the magic of list references, this will modify the original
        #   amount in the original list
        creditor[1] = new_amount

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name

class Graph:
    def __init__(self, node_list):
        self.nodes = node_list

    def get_nodes(self):
        return self.nodes

    def _tarjan(self, removed=None):
        removed = set() if removed is None else removed
        overall_id = 0
        treated_nodes = {node: -1 for node in self.nodes if node not in removed}
        lowest_backedge = {node: 0 for node in self.nodes if node not in removed}
        node_stack = []
        sccs = []

        for node in self.nodes:
            if (node not in removed) and (treated_nodes[node] == -1):
                self._tarjan_explore(node, overall_id, treated_nodes, lowest_backedge, node_stack, sccs)

        return sccs

    def _tarjan_explore(self, curr_node, overall_id, treated_nodes, lowest_backedge, node_stack, sccs):
        overall_id +=1
        my_min = overall_id
        treated_nodes[curr_node] = lowest_backedge[curr_node] = overall_id
        node_stack.append(curr_node)

        for child in curr_node.get_creditors():
            if child in treated_nodes: # Checks if the child was not in the removed set
                if treated_nodes[child] == -1:
                    self._tarjan_explore(child, overall_id, treated_nodes, lowest_backedge, node_stack, sccs)
                my_min = min(my_min, lowest_backedge[child])

        if my_min < lowest_backedge[curr_node]:
            lowest_backedge[curr_node] = my_min
        else:
            current_scc = []

            popped_node = node_stack.pop()
            current_scc.append(popped_node)
            while popped_node != curr_node:
                popped_node = node_stack.pop()
                current_scc.append(popped_node)
                lowest_backedge[popped_node] = infinity

            sccs.append(current_scc)

    def simplify_debts(self):
        pass


class CommunityFinder:
    """
    Finds the chains of linked nodes in the graph. 
    """
    def __init__(self,graph):
        self.graph = graph
        self.nodes = self.graph.get_nodes()
        self.communities = self.find_communities()

    def __repr__(self):
        return str(self.communities)

    def find_communities(self):
        communityList = []
        communityIndex = -1     #no communities yet

        for root in self.nodes:

            if len(communityList) == 0:
                communityList.append([])    #begin first community
                communityIndex+=1           #updade current community index
                communityList[communityIndex].extend(list(set(root.get_all_related()))) #add first elements
            else:
                if not self.related(root,communityList[communityIndex]):
                #as node not related to other, new community detected
                    if len(communityList) <= communityIndex +1:
                        #print("Detected new community...")
                        communityList.append([root])
                        communityIndex+=1
                    else:
                        communityList[communityIndex].append(node)
                else:   #add nodes in debtor/creditor relation with current root node.
                    for node in root.get_all_related():
                        if not node in communityList[communityIndex]:
                                communityList[communityIndex].append(node)
        return communityList

    def get_communities(self):
        return self.communities

    def related(self,node,node_list):
        """
        Checks if node is related to any node in node_list (debtor or creditor)
        """
        res = False
        for other_node in node_list:
            if node in other_node.get_all_related():
                res = True
        return res


class HubFinder:
    """
    Finds the articulation points dividing the graph in two subgraphs
    of at least K nodes each.
    """
    def __init__(self,graph,K=0):
        self.communities = CommunityFinder(graph).get_communities()
        self.min_individuals = K
        self.hubs_list = []
        for community in self.communities:
            self.time_list = [0]*len(community) #Holds loop count at wich node was visited
            self.lowest_time = [0]*len(community) #Holds lowest child values for every node
            self.visited = [False]*len(community)
            self.predecessors = [None]*len(community) #predecessors[i] is parent of community[i]
            self.visited_time = 0
            for i in range(len(community)):
                if not self.visited[i]:
                    self.get_hubs(community,i)
        print(self.hubs_list)

    def get_hubs(self,community,root=None):
        if root == None:
            root = 0
        self.time_list[root] = self.visited_time #Set "time" of visit.
        self.lowest_time[root] = self.visited_time
        self.visited_time +=1
        successors =0
        self.visited[root] = True
        #print(self.visited_time, community[root])
        #print(list(community[root].get_all_related()))
        for adj in community[root].get_all_related():
            idx = community.index(adj)

            if not self.visited[idx]:
                self.predecessors[idx] = root
                successors+=1
                self.get_hubs(community,idx)
                self.lowest_time[root] = min(self.lowest_time[root],self.lowest_time[idx])

                #If root and more than 1 child or not root and no child <-> ancestor link.
                if not self.predecessors[root] and successors > 1 or \
                 self.predecessors[root] and self.lowest_time[idx] >= self.time_list[root]:
                    
                    if community[root] not in self.hubs_list and self.min_individuals <= self.time_list[root] <= len(community)-self.min_individuals : 
                        #print("Order: ",self.time_list[root])
                        self.hubs_list.append(community[root])

            elif idx != self.predecessors[root]: #
                self.lowest_time[root] = min(self.lowest_time[root],self.time_list[idx])


"""
    def get_hubs2(self,community,root=None):
        if root == None:
            root=0
        self.visited[root] = True
        self.visited_time+=1
        self.time_list[root]= self.visited_time
        #self.lowest_time[root] = self.visited_time
        local_min = self.visited_time

        for adj in community[root].get_creditors():
            idx = community.index(adj)

            if not self.visited[idx]:

                children_min = self.get_hubs2(community,idx)
                if children_min < local_min:
                    local_min = children_min
                if children_min >= self.time_list[root]:
                    self.hubs_list.append(community[root])
            else:
                local_min = min(local_min,self.time_list[idx])

        return local_min
"""