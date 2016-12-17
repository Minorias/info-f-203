import argparse

from parser import InputParser
from graph import Graph

parser = argparse.ArgumentParser(description = "Test the Algorithms")
parser.add_argument("inputfile", help = "Enter the name of the graph input file.")
parser.add_argument("-k", nargs= 1,type = int, dest="k", default=[1], help="Choose the number K for the hub-finding algorithm. If none is entered, defaults to 1")
parser.add_argument('--simplify', dest='simplify', action='store_true', help="Enter this in order for the graph to be simplified")
parser.add_argument('--hubs', dest='hubs', action='store_true', help="Enter this for the hub-finding algorithm to be shown")
parser.add_argument('--communities', dest='communities', action='store_true', help="Enter this for the community-finding algorithm to be shown")


class Test:
    def __init__(self, inputargs):
        self.inputargs = inputargs
        self.graph = Graph(InputParser(inputargs.inputfile).graph_output())
        self.k = inputargs.k[0]
        self.launch_test()

    def launch_test(self):
        print("-"*50)
        print("Beginning test:")
        print("Original Graph:")
        self.graph.print_graph()

        if self.inputargs.simplify:
            self.graph.simplify_debts()
            print("\n2.1: Graph after debt simplification:")
            self.graph.print_graph()

        if self.inputargs.communities:
            print("\n2.2: Communities:", self.graph.find_communities())

        if self.inputargs.hubs:
            print("\n2.3: Social Hubs with k being",self.k,":", self.graph.find_hubs(self.k))


Test(parser.parse_args())