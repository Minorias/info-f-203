class Node:
    def __init__(self,name):
        self.name = name
        self.creditors = []
        self.debtors = []
        self.debt_amounts = []

    def add_creditor(self, creditor, amount):
        self.creditors.append(creditor)
        self.debt_amounts.append(amount)

    def add_debtor(self,creditor):
    	self.debtors.append(creditor)

    def get_creditors(self):
        return self.creditors

    def get_debtors(self):
    	return self.debtors

    def change_debtor_amount(self, creditor, new_amount):
        index = this.creditors.index(creditor)
        this.debt_amounts[index] = new_amount

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Node):
            return self.name == other.name
        else:
            raise NotImplementedError

class Graph:
	def __init__(self, node_list):
		self.nodes = node_list


	def simplify_debts(self):
		pass


	def find_communities(self):
		communityList = []

		for root in self.nodes:
			currentCommunity = []
			currentCommunity.append(root)
			for node in self.nodes:
				if node in root.get_debtors() or node in root.get_creditors():
					currentCommunity.append(node)
					
			if len(communityList) > 0:
				for community in communityList:
					if set(currentCommunity) != set(community):			
						communityList.append(currentCommunity)

		return communityList

