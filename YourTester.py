import argparse

from parser import InputParser
from graph import Graph


parser = argparse.ArgumentParser(description = "Test the implemented Algorithms")
parser.add_argument("inputfile", help = "Enter the name of the graph input file.")
parser.add_argument("-k", nargs= 1,type = int, dest="k", default=[1], help="Choose the number K for the hub-finding algorithm. If none is entered, defaults to 1")
parser.add_argument('--simplify', dest='simplify', action='store_true', help="Enter this in order for the graph to be simplified")
parser.add_argument('--hubs', dest='hubs', action='store_true', help="Enter this for the hub-finding algorithm to be shown")
parser.add_argument('--communities', dest='communities', action='store_true', help="Enter this for the community-finding algorithm to be shown")
parser.add_argument('-a', '--all', dest='all', action='store_true', help="Enter this for all algorithms to be shown")


class Tester:
    def __init__(self, inputargs):
        self.graph = Graph(InputParser(inputargs.inputfile).graph_output())
        self.k = inputargs.k[0]

        if inputargs.all:
            self.simplify = True
            self.communities = True
            self.hubs = True
        else:
            self.simplify = inputargs.simplify
            self.communities = inputargs.communities
            self.hubs = inputargs.hubs

        self._launch_test()

    def _launch_test(self):
        print("-"*50)
        print("Beginning test:")
        print("Original Graph:")
        self.graph.print_graph()

        if self.simplify:
            self.graph.simplify_debts()
            print("\n2.1: Graph after debt simplification:")
            self.graph.print_graph()

        if self.communities:
            print("\n2.2: Communities:", self.graph.find_communities())

        if self.hubs:
            print("\n2.3: Social Hubs with k being",self.k,":", self.graph.find_hubs(self.k))

if __name__ == "__main__":
    Tester(parser.parse_args())