from parser import InputParser
from graph import Graph, Node, HubFinder,CommunityFinder


graph = Graph(InputParser("data.txt").graph_output())
#communities = CommunityFinder(graph)
print(CommunityFinder(graph))
hubs =  HubFinder(graph)