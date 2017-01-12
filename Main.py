MAX = 9999999999999.0

import bellman_ford as bl
import EdmondsKarp as ek
import parsing as ps


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
    VarList['c' + str(0) + str(2)] = 80


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

    VarList = ek.Compute_Flow_EdmondsKarp(5,0,4,EdgeList,VarList,6)
    for Edge in EdgeList:
        print 'Initial Flow in ',Edge[0],', ',Edge[1],'is : ',VarList['x'+str(Edge[0])+str(Edge[1])]

    [E1, Residual_Network] =  ek.Compute_Residual_Network(5, EdgeList, VarList)
    Neg_Path = bl.Bellman_Ford(E1,Residual_Network,5)
    count = 0
    print Neg_Path[1]
    while Neg_Path[0] == True:
            print 'Count: ',count
            MinCap = MAX
            for Edge in Neg_Path[1]:
                if (MinCap < Residual_Network['u'+str(Edge[0]) + str(Edge[1])]):
                    MinCap =  Residual_Network['u'+str(Edge[0]) + str(Edge[1])]
            print 'Minimum Capacity', MinCap
            if MinCap != MAX:
                for Edge in Neg_Path[1]:
                    [a,b] = [Edge[0],Edge[1]]
                    if [a,b] in EdgeList:
                        VarList['x' + str(a) + str(b)] = Residual_Network['x' + str(a) + str(b)] + MinCap;
                    if ([b, a] in E1) and ([b,a] not in EdgeList):
                        VarList['x' + str(a) + str(b)] = Residual_Network['x' + str(a) + str(b)] - MinCap;

            for Edge in EdgeList:
                print 'Flow in ', Edge[0], ', ', Edge[1], 'is : ', VarList['x' + str(Edge[0]) + str(Edge[1])]

            [E1, Residual_Network] = ek.Compute_Residual_Network(5,EdgeList,VarList)
            Neg_Path = bl.Bellman_Ford(E1, Residual_Network, 5)
            print Neg_Path[1]
            count = count + 1

    for Edge in EdgeList:
        print ('Flow  in Edges: ',Edge[0],Edge[1],'is: ',VarList['x'+str(Edge[0])+str(Edge[1])])

Test()