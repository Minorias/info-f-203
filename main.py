from parser import InputParser
from graph import Graph, Node, HubFinder


graph = Graph(InputParser("data.txt").graph_output())
print(graph.find_communities())
print(graph.find_hubs())
# print("Communities: ",graph.find_communities())
# print("Strongly Connected Components: ",graph.find_sccs())
# print("Cycles: ", graph.find_cycles())
# print()
# print("BEFORE SIMPLIFICATIONS")
# graph.ouput_graph()
# graph.simplify_debts()
# print()
# print("AFTER SIMPLIFICATIONS")
# graph.ouput_graph()
