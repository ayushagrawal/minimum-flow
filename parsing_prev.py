
# Incomplete.....Cost and supply vectors need to be added



# This code parses the user inputed graph into its corresponding fanin list, cost of
# edges list, supply and demand of the nodes
# The user must input the supply and demand according to the numbering in the graph
# The numbers used must be from (0-n) and only arrows '->' and count edge only once

input_string = "0->4->3,0->6->2->3,0->1,0->2,6->1,6->4,5->2"
print(input_string)


# Calculating the number of nodes in the graph
num_nodes = len(set(input_string.replace('->',' ').replace(',',' ').split()))
print(num_nodes)
fanin = [[] for i in range(num_nodes)]
#parsing starts
edge_list = input_string.split(',')  # return a list of edges in string format
for edge_string in edge_list:
    single_edge_string = edge_string.split('->')
    for element in range(len(single_edge_string)-1):
        fanin[int(single_edge_string[element+1])].append(int(single_edge_string[element]))

print(fanin)
