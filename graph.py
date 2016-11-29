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

