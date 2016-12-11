from parser import InputParser
from graph import Graph, Node


graph = Graph(InputParser("data.txt").graph_output())
print("Communities: ",graph.find_communities())
print("Strongly Connected Components: ",graph.find_sccs())
print("Cycles: ", graph.find_cycles())
print()
print("BEFORE SIMPLIFICATIONS")
graph.ouput_graph()
graph.simplify_debts()
print()
print("AFTER SIMPLIFICATIONS")
graph.ouput_graph()