MAX = 9999999999999
import numpy as np

# Initialize a flow in the graph. Arguments are number of nodes, source node, sink node,
# list of Edges, list of  variables of cost,capacity and flow for each variable and the flow required
def Compute_Flow_EdmondsKarp(N,source,sink,EdgeList,VarList,f):
    Total_Flow = 0
    # Generate a residual network with the edgelist and corresponding dictionary of variables
    [E_Residual,Residual_VarList] = Compute_Residual_Network(N,EdgeList,VarList)

    # Find a path between the source and sink with non maximum flow.
    while Find_Augmenting_Path(N,source,sink,E_Residual,EdgeList,Residual_VarList) != None and Total_Flow < f:
        Path = Find_Augmenting_Path(N,source,sink,E_Residual,EdgeList,Residual_VarList)
        Min = MAX
        Min_Edge = [-1,1]
        for i in range(len(Path)-1):
            Edge = [Path[i], Path[i + 1]]
            if Min > Residual_VarList['u'+str(Edge[0])+str(Edge[1])]:
                Min = Residual_VarList['u'+str(Edge[0])+str(Edge[1])]
                Min_Edge = Edge
        if Total_Flow + Min > f:
            Min = f-Total_Flow

        print ('Flow added in the Path',Path)
        print ('Total Flow added: ', Min)

        Total_Flow = Total_Flow + Min
        if Path != None:
            for i in range(len(Path)-1):
                Edge = [Path[i], Path[i + 1]]
                VarList['x'+str(Edge[0])+str(Edge[1])] = VarList['x'+str(Edge[0])+str(Edge[1])] + Min
                Residual_VarList['u' + str(Edge[0]) + str(Edge[1])] = Residual_VarList['u' + str(Edge[0]) + str(Edge[1])] - Min

    return VarList





# Return an edge list and corresponding dictionary of the Residual graph.
def Compute_Residual_Network(N,EdgeList,VarList):
    E1 = list()
    Residual_VarList = dict()

    for Edge in EdgeList:
        [a,b] = Edge[0],Edge[1]

        E1.append([a,b])
        Residual_VarList['u' + str(a) + str(b)] = VarList['u' + str(a) + str(b)] - VarList['x' + str(a) + str(b)]
        Residual_VarList['c' + str(a) + str(b)] = VarList['c' + str(a) + str(b)]

        E1.append([b,a])
        Residual_VarList['u' + str(b) + str(a)] = VarList['x' + str(a) + str(b)]
        Residual_VarList['c' + str(b) + str(a)] = -VarList['c' + str(a) + str(b)]


    return [E1,Residual_VarList]


def Find_Augmenting_Path(Nodes,source,sink,E_Residual,EdgeList,VarList):
    Path = list()
    Parent = -1 * np.ones(Nodes, dtype='int')
    MinDist = 1000 * np.ones(Nodes, dtype='int')
    MinDist[source] = 0

    Nodes_To_Vist = list()
    for i in range(Nodes):
        Nodes_To_Vist.append(i)

    while len(Nodes_To_Vist) > 0:
        MinDistance = MAX
        for i in range(Nodes):
            if i in Nodes_To_Vist and MinDistance > MinDist[i]:
                MinDistance = MinDist[i]
                Current_Node = i
        Nodes_To_Vist.remove(Current_Node)
        # Create the Fanout List of current Node

        for Edge in EdgeList:
            Cap_Edge = VarList['u' + str(Edge[0]) + str(Edge[1])]
            if Edge[0] == Current_Node and Cap_Edge > 0:
                Alt = MinDist[Current_Node] + Cap_Edge
                if Alt < MinDist[Edge[1]]:
                    Parent[Edge[1]] = Current_Node
                    MinDist[Edge[1]] = Alt

    nextNode = sink
    Path.append(sink)
    while Parent[nextNode]  != -1:
        Path.insert(0,Parent[nextNode])
        nextNode = Parent[nextNode]


    if Path[0] == source:
        return Path
    else:
        print ('No augmenting Path')
        return None
#


def Test():
    EdgeList = list()
    VarList = dict()

    EdgeList.append([0, 1])
    VarList['u' + str(0) + str(1)] = 3
    VarList['x' + str(0) + str(1)] = 0
    VarList['c' + str(0) + str(1)] = 20

    EdgeList.append([1, 2])
    VarList['u' + str(1) + str(2)] = 5
    VarList['x' + str(1) + str(2)] = 0
    VarList['c' + str(1) + str(2)] = 50

    EdgeList.append([0, 2])
    VarList['u' + str(0) + str(2)] = 4
    VarList['x' + str(0) + str(2)] = 0
    VarList['c' + str(0) + str(2)] = 4


    EdgeList.append([0, 3])
    VarList['u' + str(0) + str(3)] = 2
    VarList['x' + str(0) + str(3)] = 0
    VarList['c' + str(0) + str(3)] = 0



    EdgeList.append([2, 3])
    VarList['u' + str(2) + str(3)] = 4
    VarList['x' + str(2) + str(3)] = 0
    VarList['c' + str(2) + str(3)] = 10

    EdgeList.append([1, 3])
    VarList['u' + str(1) + str(3)] = 3
    VarList['x' + str(1) + str(3)] = 0
    VarList['c' + str(1) + str(3)] = 40

    EdgeList.append([1, 4])
    VarList['u' + str(1) + str(4)] = 9
    VarList['x' + str(1) + str(4)] = 0
    VarList['c' + str(1) + str(4)] = 100


    EdgeList.append([3, 4])
    VarList['u' + str(3) + str(4)] = 7
    VarList['x' + str(3) + str(4)] = 0
    VarList['c' + str(3) + str(4)] = 10



    # P = Find_Augmenting_Path(5,0,4,EdgeList,VarList)
    # print P
    VarList = Compute_Flow_EdmondsKarp(5,0,4,EdgeList,VarList,8)
    for Edge in EdgeList:
        print ('Flow in ',Edge[0],', ',Edge[1],'is : ',VarList['x'+str(Edge[0])+str(Edge[1])])

Test()