from math import inf as infinity
from copy import copy

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
                self._explore(node)

        return self.sccs

    def _explore(self,curr_node):
        self.overall_id +=1
        my_min = self.overall_id
        self.treated_nodes[curr_node] = self.lowest_backedge[curr_node] = self.overall_id
        self.node_stack.append(curr_node)

        for child in curr_node.get_creditors():
            if (child in self.nodes) and (child not in self.removed_set):
                if self.treated_nodes[child] == -1:
                    self._explore(child)
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
                self._find_cycles(starting_node, starting_node, set(current_scc))
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

    def _find_cycles(self, starting_node, current_node, current_scc):
        found_cycle = False
        self.node_stack.append(current_node)
        self.blocked_set.add(current_node)
        for child in current_node.get_creditors():
            if child in current_scc:
                if child == starting_node: #We have completed a cycle
                    self.allcycles.append(self.node_stack[::])
                    self.allcycles[-1].append(starting_node)
                    found_cycle = True

                elif child not in self.blocked_set:
                    found_cycle = self._find_cycles(starting_node, child, current_scc) or found_cycle

        if found_cycle:
            self._unblock(current_node)
        else:
            for child in current_node.get_creditors():
                if child in current_scc:
                    if child in self.blocked_map:
                        self.blocked_map[child].append(current_node)
                    else:
                        self.blocked_map[child] = [current_node]

        self.node_stack.pop()

        return found_cycle

    def _unblock(self, node):
        self.blocked_set.remove(node)
        if node in self.blocked_map:
            for other_node in self.blocked_map[node]:
                if other_node in self.blocked_set:
                    self._unblock(other_node)
            self.blocked_map.pop(node)


class Communities:
    """
    Finds all related node groups <=> All connected subgraphs
    """
    def __init__(self, node_list):
        self.nodes = node_list

        self.communitylist = []
        self.visited = {node: -1 for node in self.nodes}

    def find_communities(self):
        """
        Calls dfs from every node in order to separate related/unrelated nodes.
        """
        for node in self.nodes:
            if self.visited[node] == -1:
                self.communitylist.append([])
                self._explore(node)

        return self.communitylist

    def _explore(self, node):
        """
        Depth first search?
        """
        self.visited[node] = 1
        self.communitylist[-1].append(node)
        for related in node.get_all_related():
            if self.visited[related] == -1:
                self._explore(related)


class HubFinder:
    """
    Finds the articulation points dividing the graph in subgraphs
    of at least K nodes each.
    """
    def __init__(self,nodes,K=2):
        self.k = K              #Minimum length of subcommunities.
        self.hubs_list = []
        self.nodes = nodes

        self.time_list = {}      #contains the time a node has been explored
        self.lowest_time = {}    #contains the lowest time of a node's successors
        self.visited = {}        #tells if a node has been visited or not
        self.predecessors = {}   #stores a reference to a node's parent node

        self.dfs_visited = set()

    def get_hubs(self):
        """
        Calls the hub finder for every community in graph.
        """
        for community in Communities(self.nodes).find_communities():
            self.time_list = {node : 0 for node in community}
            self.lowest_time = {node : 0 for node in community}
            self.visited = {node : False for node in community}
            self.predecessors = {node : None for node in community}
            self.visited_time = 0

            for node in community:
                if self.visited[node] is False:
                    self._explore_hub(community,node)

        self._check_k()
        return self.hubs_list

    def _explore_hub(self,community,root):
        """
        Finds the hubs in a given community. Implements a depth first search.
        """
        self.time_list[root] = self.visited_time #Set "time" of visit.
        self.lowest_time[root] = self.visited_time
        self.visited_time +=1
        successors = 0      #number of children of a node
        self.visited[root] = True

        for adj in root.get_all_related():
            if self.visited[adj] is False:
                self.predecessors[adj] = root
                successors+=1
                self._explore_hub(community,adj)
                self.lowest_time[root] = min(self.lowest_time[root],self.lowest_time[adj])

                #If treeroot and more than 1 child or not root and no back edge.
                if ((self.predecessors[root] is None and successors > 1) or
                    (self.predecessors[root] is not None and self.lowest_time[adj] >= self.time_list[root])):

                    if root not in self.hubs_list:
                        self.hubs_list.append(root)

            elif adj != self.predecessors[root]: #
                self.lowest_time[root] = min(self.lowest_time[root],self.time_list[adj])

    def _check_k(self):
        """
        Updates the hubs_list by removing the hubs splitting graph in sections of size < K
        """
        for i in range(len(self.hubs_list)-1, -1, -1):
            hub = self.hubs_list[i]

            lengths = []
            for community_start_point in hub.get_all_related():
                self.dfs_visited.add(hub)
                self._dfs(community_start_point)
                #Subtract one since we added the articulation point to the set aswell
                lengths.append(len(self.dfs_visited) - 1)
                self.dfs_visited = set()

            if not all(x >= self.k for x in lengths):
                self.hubs_list.remove(hub)



    def _dfs(self, current_node):
        """
        Depth first search.
        """
        self.dfs_visited.add(current_node)
        for related in current_node.get_all_related():
            if related not in self.dfs_visited:
                self._dfs(related)
