from parser import InputParser
from graph import Graph, Node, HubFinder


graph = Graph(InputParser("data.txt").graph_output())
print(graph.find_communities())
hubs =  HubFinder(graph.get_nodes())