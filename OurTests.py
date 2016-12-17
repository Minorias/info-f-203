from graph import Graph
from parser import InputParser

print("-"*100)
print("Testing Graph Simplification: ")

graph1 = Graph(InputParser("oursimplificationtest1.txt").graph_output())
print("-"*50)
print("Test 1: ")
print("Original Graph:")
graph1.print_graph()
graph1.simplify_debts()
print("\nGraph after simplification:")
graph1.print_graph()
print()

graph1 = Graph(InputParser("oursimplificationtest2.txt").graph_output())
print("-"*50)
print("Test 2: ")
print("Original Graph:")
graph1.print_graph()
graph1.simplify_debts()
print("\nGraph after simplification:")
graph1.print_graph()
print("\n\n")




print("-"*100)
print("Testing Community Finding: ")

graph1 = Graph(InputParser("ourcommunitiestest1.txt").graph_output())
print("-"*50)
print("Test 1: ")
print("Original Graph:")
graph1.print_graph()
print("\nCommunities:", graph1.find_communities())
print("\n\n")

print("-"*100)
print("Testing Hub Finding: ")

graph1 = Graph(InputParser("ourhubstest1.txt").graph_output())
print("-"*50)
print("Test 1: ")
print("Original Graph:")
graph1.print_graph()
print("\nHubs with k being 1:", graph1.find_hubs(1))
print("Hubs with k being 2:", graph1.find_hubs(2))
print("Hubs with k being 3:", graph1.find_hubs(3))
print("Hubs with k being 4:", graph1.find_hubs(4))