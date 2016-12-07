from itertools import chain
from math import inf as infinity
from copy import copy

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


class SCCs_Tarjan:
    """
    Implementation of Tarjan's algorithm for finding all strongly connected components
    within a graph

    A slight modification of the algorithm shown in the syllabus in order to immediately
    place the nodes that make up a component into a list rather than using a vector to class them
    """
    def __init__(self, node_list, removed_set):
        self.nodes = node_list
        self.removed_set = removed_set
        self.overall_id = 0
        self.treated_nodes = {node: -1 for node in self.nodes if node not in self.removed_set}
        self.lowest_backedge = {node: 0 for node in self.nodes if node not in self.removed_set}
        self.node_stack = []
        self.sccs = []

    def find_sccs(self):
        for node in self.nodes:
            if (node not in self.removed_set) and (self.treated_nodes[node] == -1):
                self.explore(node)

        return self.sccs

    def explore(self,curr_node):
        self.overall_id +=1
        my_min = self.overall_id
        self.treated_nodes[curr_node] = self.lowest_backedge[curr_node] = self.overall_id
        self.node_stack.append(curr_node)

        for child in curr_node.get_creditors():
            if (child in self.nodes) and (child not in self.removed_set):
                if self.treated_nodes[child] == -1:
                    self.explore(child)
                my_min = min(my_min, self.lowest_backedge[child])

        if my_min < self.lowest_backedge[curr_node]:
            self.lowest_backedge[curr_node] = my_min
        else:
            current_scc = []

            condition = True
            while condition:
                popped_node = self.node_stack.pop()
                if popped_node == curr_node:
                    condition = False
                current_scc.append(popped_node)
                self.lowest_backedge[popped_node] = infinity

            self.sccs.append(current_scc)


class Cycles_Johnson:
    """
    Implementation of the Johnson's algorithm for finding and enumerating all
    elementary cycles within a graph.

    http://people.cs.vt.edu/~gback/ICPCHandbook/book/copiesfromweb/circuits_johnson.pdf
    """
    def __init__(self, node_list):
        self.nodes = node_list
        self.node_stack = []

        self.removed_set = set()
        self.blocked_set = set()
        self.blocked_map = {}
        self.allcycles = []

    def get_cycles(self):
        # List of all the strongly connected components of the graph
        all_sccs = SCCs_Tarjan(self.nodes, self.removed_set).find_sccs()

        # We look at each strongly connected subgraph, looping over the list until
        #   reaching the end as the list may grow in size as the components can break
        #   up into several others that are appended at the end
        i = 0
        while i < len(all_sccs):
            current_scc = all_sccs[i]
            while len(current_scc) > 1:
                starting_node = current_scc[0]
                                                               #convert it to a set for faster lookup in the future
                self.find_cycles(starting_node, starting_node, set(current_scc))
                self.removed_set.add(starting_node)
                # We remove the starting node and recalculate the strongly connected components
                #   if this happens to break the current scc into several we take the first one
                #   to work on and add the rest to the end of the list of all the other sccs
                possibly_many_sccs = SCCs_Tarjan(current_scc, self.removed_set).find_sccs()
                current_scc = possibly_many_sccs[0]
                all_sccs.extend(possibly_many_sccs[1:])

                self.blocked_map.clear()
                self.blocked_set.clear()

            i+=1
            self.removed_set.clear()

        return self.allcycles

    def find_cycles(self, starting_node, current_node, current_scc):
        found_cycle = False
        self.node_stack.append(current_node)
        self.blocked_set.add(current_node)
        for child in current_node.get_creditors():
            if child not in self.removed_set and child in current_scc:
                if child == starting_node: #We have completed a cycle
                    self.allcycles.append(self.node_stack[::-1])
                    found_cycle = True

                elif child not in self.blocked_set:
                    found_cycle = self.find_cycles(starting_node, child, current_scc) or found_cycle

        if found_cycle:
            self.unblock(current_node)
        else:
            for child in current_node.get_creditors():
                if child not in self.removed_set and child in current_scc:
                    if child in self.blocked_map:
                        self.blocked_map[child].append(current_node)
                    else:
                        self.blocked_map[child] = [current_node]

        self.node_stack.pop()

        return found_cycle

    def unblock(self, node):
        self.blocked_set.remove(node)
        if node in self.blocked_map:
            for other_node in self.blocked_map[node]:
                if other_node in self.blocked_set:
                    self.unblock(other_node)
            self.blocked_map.pop(node)


class Graph:
    def __init__(self, node_list):
        self.nodes = node_list

    def find_sccs(self):
        tarjan = SCCs_Tarjan(self.nodes, set())
        return tarjan.find_sccs()

    def find_cycles(self):
        cycles = Cycles_Johnson(self.nodes).get_cycles()
        return cycles

    def simplify_debts(self):
        pass


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

        #print(communityList)
        return communityList

    def related(self,node,node_list):
        """
        Checks if node is related to any node in node_list (debtor or creditor)
        """
        res = False
        for other_node in node_list:
            if node in other_node.get_all_related():
                res = True
        return res
