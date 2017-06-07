    
    
def logicExpGraph(string):
    
    import pydot as py
    
    # the priority level table
    numVars = 0
    operations = 0
    varDict = dict()
    priorityLevel = {'+':0 , '$':0, '*':1 , '!':2, '^':1, '#':1, '(':-2, '=':-1}
    # + : or
    # $ : nor 
    # * : and
    # ! : not 
    # ^ : xor
    # # : nand
    
    # defining the getPriority function
    def get_priority(i):
        return priorityLevel[i]
    
    # Now we first calculate the post fix expression from the infix operation
    
    def infixToPostfix(string):
        exp = ""
        stack = list()
        bracketNum = 0
        validity = 0
        global numVars
        global operations
        for i in string:
            if(i.isalnum()):
                if(i not in exp):
                    numVars = numVars + 1
                exp = exp + i
                validity = validity + 1  
                
            else:
                if(i == "("):
                    bracketNum = bracketNum + 1
                    stack.append(i)
                elif(i == ")"):
                    if(bracketNum == 0):
                        return "Invalid Expression"
                    bracketNum = bracketNum - 1
                    
                    while(1):
                        if(stack[-1] == "("):
                            stack.pop()
                            break
                        exp = exp + stack.pop()
                        
                else:
                    operations = operations + 1
                    if(stack != []):
                        while(get_priority(i) <= get_priority(stack[-1])):
                            exp = exp + stack.pop()
                            if(stack == []):
                                break
                        stack.append(i)
                        validity = validity - 1
                    else:
                        validity = validity - 1
                        stack.append(i)
            
        if((validity != 1) or (bracketNum !=0)):
            return "Invalid Expression"        
        while(stack != []):
             exp = exp + stack.pop()      
        return exp
    
    # Make each binary operation to be a new node
    
    str2 = string
    str1 = infixToPostfix(str2)
    print(str1)
    print(numVars)
    print(operations)
    
     #converting the postfix to expression tree 
    def postfixToExpression(string):
        global numVars
        node_name1 = 0
        node_name2 = numVars 
        fanin = [None for i in range(numVars + operations)]
        stack = list()
        
        if(string == "Invalid Expression"):
            return []
        else:
            # The input variables will be counted from node 0
            for i in string:
                if(i.isalnum()):
                    if(i not in varDict.values()):
                        varDict[node_name1] = i
                        stack.append(node_name1)
                        node_name1 = node_name1 + 1 
                    else:
                        stack.append(list(varDict.keys())[list(varDict.values()).index(i)])
                else:
                    varDict[node_name2] = i
                    fanin[node_name2] = [stack.pop(),stack.pop()]
                    stack.append(node_name2)
                    node_name2 = node_name2 + 1
            
            return fanin
                    
    fanin = postfixToExpression(str1)
    print(fanin)
    print(varDict)
    
    # plotting the expression tree
    graph = py.Dot(graph_type = 'digraph')
    node  = [None for i in range(2*numVars - 1)]
    for i in range(len(fanin)):
        if(fanin[i] == None):
            graph.add_node(py.Node(i, style="filled", fillcolor="blue",label = varDict[i] ))
        else:
             graph.add_node(py.Node(i, style="filled", fillcolor="green",label = varDict[i] ))
             graph.add_edge(py.Edge(i, fanin[i][0]))
             graph.add_edge(py.Edge(i, fanin[i][1]))
    graph.write_jpg("expressionTree.jpg")
    
   
    
    s = 0                       #Source node, Also the 0th index always correspond to one of the source node
    t = len(fanin) - 1          # Terminal node, As the last node is always the terminal node in our algorithm
     
    fixedCells = list()
    for i in range(len(varDict)):
        if(varDict[i].isalnum()):
            fixedCells.append(i)

    return fanin,fixedCells