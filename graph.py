class Node:
    def __init__(self,name):
        self.name = name
        self.debtors = []
        self.creditors = []
        self.debt_amounts = []

    def add_debtor(self, debtor, amount):
        self.debtors.append(debtor)
        self.debt_amounts.append(amount)
        
    def add_creditor(self,creditor):
    	self.creditors.append(creditor)

    def get_debtors(self):
        return self.debtors

    def get_creditors(self):
    	return self.creditors

    def change_debtor_amount(self, debtor, new_amount):
        index = this.debtors.index(debtor)
        this.debt_amounts[index] = new_amount

    def __eq__(self, other_name):
        return self.name == other_name

class Graph:
    def __init__(self, node_list):
        self.nodes = node_list


    def simplify_debts(self):
        pass


    def find_communities(self):
    	
    	for node in self.nodes:
