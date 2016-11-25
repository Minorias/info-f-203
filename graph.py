class Node:
    def __init__(self,name):
        self.name = name
        self.creditors = []
        self.debtors = []

    def add_creditor(self, creditor, amount):
        self.creditors.append([creditor, amount])

    def add_debtor(self,creditor):
    	self.debtors.append(creditor)

    def get_creditors(self):
        return [creditor[0] for creditor in self.creditors]

    def get_debtors(self):
    	return self.debtors

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

