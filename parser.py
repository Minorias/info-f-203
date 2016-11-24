from graph import Node

class InputParser:
    def __init__(self, filename):
        self.filename = filename
        self.node_list = []
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
                self.node_list.append(node_2)

            if node_1 is None:
                node_1 = Node(datapoint[0])
                self.node_list.append(node_1)

            node_1.add_debtor(node_2, amount)
            node_2.add_creditor(node_1)

    def get_node(self,name):
        try:
            return self.node_list[self.node_list.index(name)]
        except ValueError:
            return None

    def graph_output(self):
        return self.node_list