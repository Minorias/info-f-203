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

    def get_nodes(self):
        return self.nodes

    def find_sccs(self):
        return SCCs_Tarjan(self.get_nodes(), set()).find_sccs()

    def find_cycles(self):
        return Cycles_Johnson(self.get_nodes()).get_cycles()

    def find_hubs(self, k):
        return HubFinder(self.get_nodes(), k).get_hubs()

    def find_communities(self):
        return Communities(self.get_nodes()).find_communities()

    def simplify_debts(self):
        """
        Simplifies the debts among a group of friends.
        First enumerates all the simple cycles contained within the graph,then
            iterates over them, finding the minimum debt contained within and
            subtracting it from all debts in that cycle.

        In some cases, slightly different results may be possible due to the
            order in which the cycles are simplified.
        """
        cycles = Cycles_Johnson(self.get_nodes()).get_cycles()

        for cycle in cycles:
            # We start the debt at infinity so any debt value will be taken when
            #  when we first take the minimum.
            debt_to_simplify = infinity

            # Traverse the cycle finding the minimal debt within it
            for i in range(len(cycle) - 1):
                current_node = cycle[i]
                next_node = cycle[i+1]
                debt_to_simplify = min(debt_to_simplify, current_node.get_creditor_amount(next_node))

            # Traverse the cycle once again, this time subtracting the minimal
            #  debt from all others
            for i in range(len(cycle) - 1):
                current_node = cycle[i]
                next_node = cycle[i+1]

                current_node.reduce_creditor_amount(next_node, debt_to_simplify)

    def print_graph(self):
        """
        Prints out the graph in the same format as the input file had it
        """
        for node in self.get_nodes():
            for creditor in node.get_creditors():
                print(node, creditor, node.get_creditor_amount(creditor))
