from parser import InputParser
from graph import Graph, Node


graph = Graph(InputParser("data.txt").graph_output())
print(graph.find_communities())