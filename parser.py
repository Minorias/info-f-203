class Node:
    def __init__(self,name, debtor=None, debt_amount=None):
        self.name = name
        self.debtors = []
        self.debt_amounts = []

    def add_debtor(self, debtor, amount):
        self.debtors.append(debtor)
        self.debt_amounts.append(amount)

    def get_debtors(self):
        return self.debtors

    def change_debtor_amount(self, debtor, new_amount):
        index = this.debtors.index(debtor)
        this.debt_amounts[index] = new_amount


class InputParser:
    def __init__(self, filename):
        self.filename = filename
        self.node_dictionaty = {}
        self.parse()
        self.create_nodes()

    def parse(self):
        data = open(self.filename, "r").read().split("\n")
        self.data = [line.split(" ") for line in data][1:]

    def create_nodes(self):
        for datapoint in self.data:
            node_1 = self.get_node(datapoint[0])
            node_2 = self.get_node(datapoint[1])
            amount = int(datapoint[2])

            if node_2 is None:
                node_2 = Node(datapoint[1])
                self.node_dictionaty[datapoint[1]] = node_2

            if node_1 is None:
                node_1 = Node(datapoint[0])
                self.node_dictionaty[datapoint[0]] = node_1

            node_1.add_debtor(node_2, amount)

        for key,item in self.node_dictionaty.items():
            print(key, item.name, [debtor.name for debtor in item.debtors])


    def get_node(self,name):
        try:
            return self.node_dictionaty[name]

        except KeyError:
            return None

InputParser("data.txt")