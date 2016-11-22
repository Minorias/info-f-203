class Node:
    def __init__(self,name):
        self.name = name
        self.debtors = []

    def add_debtor(self, debtor, amount):
        self.debtors.append([debtor, amount])

    def get_debtors(self):
        return self.debtors

    def change_debtor_amount(self, debtor, new_amount):
        index = this.debtors.indexgit (debtor)
        this.debt_amounts[index] = new_amount

    def __eq__(self, other_name):
        return self.name == other_name


class Graph:
    def __init__(self, node_list):
        self.nodes = node_list


    def simplify_debts(self):
        pass

