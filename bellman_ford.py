# Author : Pratik and Ayush
# Title  : Bellman Ford algorithm
# Purpose : To find the negative cycle in the graph. It returns the predecessor for 
# every node in the shortest path and detectes the presence of negative cycle
            


MAX = 9999999999999

from parsing import parsing

edgeList = list()
varList = dict()

def Test():
    global edgeList;
    global varList;
    global num_nodes
    input_string = "(0->3,10,5);(0->1,10,5);(1->2,10,5);(3->4,10,5);(4->5,10,5);(2->5,10,5);(5->8,10,5);(8->6,-10,5);(6->4,-30,5)(7->6,10,5);(4->7,10,5)"
    num_nodes    = 9 
    # print(input_string)

    #parsing starts

    [edgeList, varList] = parsing(input_string)
    
   
def Bellman_Ford(edgeList,varList,num_nodes):
    
    # print('The list of edges is : ',edgeList)
    # print('The capacity and cost of edges are : ',varList)
    # print('The number of nodes are : ',num_nodes)
    
    ## initialising for the Bellman Ford algorithm
    cost = [MAX for i in range (num_nodes)]
    predecessor = [None for i in range (num_nodes)]
    cost[0] = 0         # As we have to just identify the presence of negativeCycle
    neg = False
    negativeCycle = list()
    
    for i in range (num_nodes-1):
        for edge in edgeList:
            if(cost[edge[1]] > cost[edge[0]] + varList['c'+str(edge[0])+str(edge[1])]):
                cost[edge[1]] = cost[edge[0]] + varList['c'+str(edge[0])+str(edge[1])]
                predecessor[edge[1]] = edge[0]
    for edge in edgeList:
        if(cost[edge[1]] > cost[edge[0]] + varList['c'+str(edge[0])+str(edge[1])]):
            neg = True
            negativeCycle.append(edge)
            v = edge[0]
            
            while True:
                u = predecessor[v]
                negativeCycle.append([u,v])
                v = u
              
                if(v == edge[1]):
                    break
                else:
                    continue
                
            break
            
    # print(cost)
    # print(predecessor)
    # print(negativeCycle)
    
    return [neg,negativeCycle]
    

# Test()
# [neg,negativeCycle] = Bellman_Ford(edgeList, varList,num_nodes)