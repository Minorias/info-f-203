from graph import Node

class InputParser:
    """
    Reads file given as parameter and creates a graph from it.
    """
    def __init__(self, filename):
        self.filename = filename
        self.node_list = []
        self.data = []

        self._parse()
        self._create_nodes()

    def _parse(self):
        try:
            data = open(self.filename, "r").read().split("\n")
            self.data = [line.split(" ") for line in data][1:]
        except FileNotFoundError:
            print("That input file does not exist")
            print("Exiting...")
            exit()

    def _create_nodes(self):
        for datapoint in self.data:
            node_1 = self._get_node(datapoint[0])
            node_2 = self._get_node(datapoint[1])
            amount = int(datapoint[2])

            if amount < 0:
                print("Debts cannot be negative")
                print("Exiting...")
                exit()

            if node_2 is None:
                node_2 = Node(datapoint[1])
                self.node_list.append(node_2)

            if node_1 is None:
                node_1 = Node(datapoint[0])
                self.node_list.append(node_1)

            node_1.add_creditor(node_2, amount)
            node_2.add_debtor(node_1)

    def _get_node(self,name):
        # Try to find node with the right name in the list of already created nodes
        found_node = [node for node in self.node_list if node.name == name]

        if found_node == []:
            # Node was found
            found_node = None
        else:
            found_node = found_node[0]

        return found_node

    def graph_output(self):
        return self.node_list