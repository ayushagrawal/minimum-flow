#####################################################


#     minimize summation of L_j_i over all i,j such that j->i
# subject to
#       0 <= x_i <= LENGTH ...... for all i
#       x_p = X_p .....for p among fixedCells
#		0 <= y_i <= LENGTH ...... for all i
#       y_p = Y_p .....for p among fixedCells
#       Lx_j_i >= x_i - x_j  ..... for j->i
#       Lx_j_i >= x_j - x_i .... for j->i
#		Ly_j_i >= y_i - y_j  ..... for j->i
#       Ly_j_i >= y_j - y_i .... for j->i
#       Lx_j_i >= minimum_separation  .... for j->i
#		Ly_j_i >= minimum_separation  .... for j->i
#       a_s = 0.0
#       a_t <= r_t
#       a_i >= a_j + delay_i + alpha * (Lx_j_i + Ly_j_i)  .... for all i,j such that j->i


# RAT_t = RAT of the terminal node
# fixedCells contains node number of inputs and outputs i.e. fixed locations
# fixedLocations contain the position of corresponding nodes
# SEP = minimum seperation between 2 points
# ALPHA = cost per unit length
# DELAY = Delay matrix of nodes
# s = source node
# t = terminal node


def twoDimLp(gridX,gridY,fanin,fixedCells):

    import cvxopt 
    #from cvxopt import matrix, solvers
    import numpy
    import matplotlib.pyplot as plt
    
    def formMatrix( fanin , fixedCells, fixedLocations):
        
        global RAT_t, grid_X, grid_Y, SEP, ALPHA, DELAY, var_map, s, t
    
        numNodes = len(fanin)
        V = range(numNodes)
        A_list = list()
        b_list = list()
        # compute the number of decision variables of the Lji type, by traversing the
        #  "fanin" information. Note that "fanin" would be a list of (sub-) lists, each
        #      such sublist would represent the collection of cells in the fanin 
        #      of a particular cell
    
        num_lji_vars = 0
        for i in fanin:
            num_lji_vars = num_lji_vars + len(i)
    
        #prepare dictionary "var_map" that associates with each "natural" decision
        #    variable, the index of the "z" variable that would corresponds to it.
    
        for i in range(numNodes):
            var_map["x_" + str(i)] = 3*i
            var_map["y_" + str(i)] = 3*i+1
            var_map["a_" + str(i)] = 3*i+2
    
        index_var = 3*len(V) 
         # .... the 'lx_j_i' and 'ly_j_i' variables will  be associated
        #     with indices 3*|V| onwards
        for i in range(numNodes):
            for j in fanin[i]:
                var_map["lx_" + str(j) + "_" + str(i)] = index_var
                var_map["ly_" + str(j) + "_" + str(i)] = index_var
                index_var = index_var + 1
      
          #prepare cost-vector in the list "cost_list"
    
        cost_list = [0 for i in range(len(var_map))] 
    
        # The cost-coefficient associated with "x_i", "y_i" and "a_i" variables is 0.0
        for i in range(numNodes):
            cost_list[var_map["x_" + str(i)]] = 0.0
            cost_list[var_map["y_" + str(i)]] = 0.0
            cost_list[var_map["a_" + str(i)]] = 0.0
    
        # The cost-coefficient associated with "Lx_j_i" and "Ly_j_i" variables is 1.0
        for i in range(numNodes):
            for j in fanin[i]:
                cost_list[var_map["lx_" + str(j) + "_" + str(i)]] = 1.0
                cost_list[var_map["ly_" + str(j) + "_" + str(i)]] = 1.0
    
        for v in range(numNodes):
            tmp_row = [0 for i in range(len(var_map))]
    
            #let us now add the constraint .....  -1.0 x_v  <=  0.0  
            #we will suitably modify tmp_row entries in appropriate places.
    
            tmp_row[var_map["x_" + str(v)]] = -1.0
            A_list.append(tmp_row)
    
    	    # let us now add the constraint .....  -1.0 y_v  <=  0.0  
            # we will suitably modify tmp_row entries in appropriate places.
    
            tmp_row = [0 for i in range(len(var_map))]
            tmp_row[var_map["y_" + str(v)]] = -1.0
            A_list.append(tmp_row)
    
            #correspondingly append the RHS ( right-hand-side ) constant, namely 0.0, of this
            #inequality to list b_list ( which represents the RHS vector "b" )
            b_list.append(0.0)
            b_list.append(0.0)
    
            tmp_row = [0 for i in range(len(var_map))]
            
            # Add the constraint .....  +1.0 x_v  <=   WIDTH 
    	    # Add the constraint .....  +1.0 y_v  <=   LENGTH
            
            tmp_row[var_map["x_" + str(v)]] = 1.0
            A_list.append(tmp_row)
            b_list.append(grid_X)
    	    # initialize tmp_row of size of var_map to be equal to zero
            tmp_row = [0 for i in range(len(var_map))]
            tmp_row[var_map["y_" + str(v)]] = 1.0
            A_list.append(tmp_row)
            b_list.append(grid_Y)
    
        # The locations of input and the output are fixed
    
        for k in fixedCells:
            # add the constraint .....  -1.0 x_k  <=    -1.0 * fixedLocation[k] .... as follows
    	    # add the constraint .....  -1.0 y_k  <=    -1.0 * fixedLocation[k] .... as follows
            tmp_row = [0 for i in range(len(var_map))]
            
            tmp_row[var_map["x_" + str(k)]] = -1.0
            b_list.append(-1.0 * fixedLocations[fixedCells.index(k)][0])
            A_list.append(tmp_row)
    
            tmp_row = [0 for i in range(len(var_map))]
            tmp_row[var_map["y_" + str(k)]] = -1.0
            b_list.append(-1.0 * fixedLocations[fixedCells.index(k)][1])
            A_list.append(tmp_row)
            
    	    # Add the constraint .....  1.0 x_k  <=    1.0 * fixedLocation[k] .... as follows
    
            tmp_row = [0 for i in range(len(var_map))]
            
            tmp_row[var_map["x_" + str(k)]] = 1.0
            b_list.append(1.0 * fixedLocations[fixedCells.index(k)][0])
            A_list.append(tmp_row)
            
            # Add the constraint .....  1.0 y_k  <=    1.0 * fixedLocation[k] .... as follows
            tmp_row = [0 for i in range(len(var_map))]
            
            tmp_row[var_map["y_" + str(k)]] = 1.0
            b_list.append(1.0 * fixedLocations[fixedCells.index(k)][1])
            A_list.append(tmp_row)
        
        for i  in range(numNodes): 
            for j in fanin[ i ]:
    	        # Initialize tmp_row of size of var_map to be equal to zero 
                tmp_row = [0 for k in range(len(var_map))]
    
                # Add the constraint .....  -1.0 lx_j_i +1.0 x_i -1.0 x_j   <=    0.0
                tmp_row[var_map["x_" + str(i)]] = 1.0
                tmp_row[var_map["x_" + str(j)]] = -1.0
                tmp_row[var_map["lx_" + str(j) + "_" + str(i)]] = -1.0
                A_list.append(tmp_row)
                b_list.append( 0.0 )
        
    	        # Initialize tmp_row of size of var_map to be equal to zero 
                tmp_row = [0 for k in range(len(var_map))]
    
                # Add the constraint .....  -1.0 ly_j_i +1.0 y_i -1.0 y_j   <=    0.0
                tmp_row[var_map["y_" + str(i)]] = 1.0
                tmp_row[var_map["y_" + str(j)]] = -1.0   
                tmp_row[var_map["lx_" + str(j) + "_" + str(i)]] = -1.0   
                A_list.append(tmp_row)   
                b_list.append( 0.0 )
    
    	        # Initialize tmp_row of size of var_map to be equal to zero   
                tmp_row = [0 for k in range(len(var_map))]
                # Add the constraint .....  -1.0 l_j_i -1.0 x_i +1.0 x_j   <=    0.0
                tmp_row[var_map["x_" + str(i)]] = -1.0   
                tmp_row[var_map["x_" + str(j)]] = 1.0   
                tmp_row[var_map["lx_" + str(j) + "_" + str(i)]] = -1.0   
                A_list.append(tmp_row)   
                b_list.append( 0.0 )
    
    	        # Initialize tmp_row of size of var_map to be equal to zero   
                tmp_row = [0 for k in range(len(var_map))]
                # Add the constraint .....  -1.0 ly_j_i -1.0 y_i +1.0 y_j   <=    0.0
                tmp_row[var_map["y_" + str(i)]] = -1.0   
                tmp_row[var_map["y_" + str(j)]] = 1.0   
                tmp_row[var_map["ly_" + str(j) + "_" + str(i)]] = -1.0   
                A_list.append(tmp_row)   
                b_list.append( 0.0 )
     
    
        for ii  in range(numNodes): 
            for jj in fanin[ ii ]:
    	        # Initialize tmp_row of size of var_map to be equal to zero   
                tmp_row = [0 for i in range(len(var_map))]
    
                # Add the constraint .....  -1.0 lx_jj_ii  <=    -1.0 * SEP
                tmp_row[var_map["lx_" + str(jj) + "_" + str(ii)]] = -1.0   
                A_list.append(tmp_row)   
                b_list.append( -1.0 * SEP )
    
    	        # Initialize tmp_row of size of var_map to be equal to zero   
                tmp_row = [0 for i in range(len(var_map))]
    
                # Add the constraint .....  -1.0 ly_jj_ii  <=    -1.0 * SEP
                tmp_row[var_map["ly_" + str(jj) + "_" + str(ii)]] = -1.0   
                A_list.append(tmp_row)   
                b_list.append( -1.0 * SEP )
    
    
        # Initialize tmp_row of size of var_map to be equal to zero     
        # Add the constraint .....  -1.0 a_s  <=    0.0 
        # Add the constraint .....  +1.0 a_s  <=    0.0 
        tmp_row = [0 for i in range(len(var_map))]
    
        tmp_row[var_map["a_" + str(s)]] = -1.0   
        A_list.append(tmp_row)   
        b_list.append( 0.0 )
        
        tmp_row = [0 for i in range(len(var_map))]
    
        tmp_row[var_map["a_" + str(s)]] = -1.0   
        A_list.append(tmp_row)   
        b_list.append( 0.0 )
      
        # Initialize tmp_row of size of var_map to be equal to zero     
        tmp_row = [0 for i in range(len(var_map))]
    
        # Add the constraint .....  +1.0 a_t  <=    RAT_t
    
        tmp_row[var_map["a_" + str(t)]] = 1.0   
        A_list.append(tmp_row)   
        b_list.append( 0.0 )
    
    
        for ii in range(numNodes): 
            for jj in fanin[ ii ]:
    	        # Initialize tmp_row of size of var_map to be equal to zero     
                tmp_row = [0 for i in range(len(var_map))]
                # Add the constraint .....  ALPHA * lx_jj_ii  +1.0 a_jj -1.0 a_ii  <=  -1.0 * DELAY[ii]
                tmp_row[var_map["a_" + str(jj)]] = 1.0   
                tmp_row[var_map["a_" + str(ii)]] = -1.0   
                tmp_row[var_map["lx_" + str(jj) + "_" + str(ii)]] = ALPHA   
                A_list.append(tmp_row)   
                b_list.append( -1.0 * DELAY[ii] )
      
        for ii  in range(numNodes): 
            for jj in fanin[ ii ]:
    	        # Initialize tmp_row of size of var_map to be equal to zero     
                tmp_row = [0 for i in range(len(var_map))]
                # Add the constraint .....  ALPHA * ly_jj_ii  +1.0 a_jj -1.0 a_ii  <=  -1.0 * DELAY[ii]
                tmp_row[var_map["a_" + str(jj)]] = 1.0   
                tmp_row[var_map["a_" + str(ii)]] = -1.0   
                tmp_row[var_map["ly_" + str(jj) + "_" + str(ii)]] = ALPHA   
                A_list.append(tmp_row)   
                b_list.append( -1.0 * DELAY[ii] )
      
        return A_list, b_list, cost_list
    
    RAT_t = 10
    grid_X = gridX
    grid_Y = gridY
    SEP = 1 
    ALPHA = 1 
    DELAY = [1 for i in range(len(fanin))]
    var_map = {}
    s = 0
    t = 0     
    
    fixedLocations = [(1,2)]
    A_l, b_l, c_l = formMatrix( fanin , fixedCells, fixedLocations) 
    
    A_matrix = cvxopt.matrix( numpy.array(A_l).transpose().tolist() )
    b_matrix = cvxopt.matrix ( b_l )
    c_matrix = cvxopt.matrix ( c_l )
    
    x_all = [ij for ij in range(grid_X)] * grid_Y
    y_all = [iij for iij in range(grid_Y)]
    y_all = numpy.repeat(y_all,grid_X)
    
    if(grid_X*grid_Y < len(fanin)):
        print("Resources are less than that required")
    elif(grid_X*grid_Y == len(fanin)):
        print("Resource requirement exactly matched")
    else:
        print("Some resources are left to be used")
    
    sol=cvxopt.solvers.lp(c_matrix,A_matrix,b_matrix, solver='glpk')
    x_co = [sol['x'][var_map['x_' + str(i)]] for i in range(len(fanin))]
    y_co = [sol['x'][var_map['y_' + str(i)]] for i in range(len(fanin))]
    plt.scatter(x_co, y_co,marker = "x", c = "r", s = 100, linewidths = 5)
    plt.scatter(x_all,y_all,marker = "o", c = "y")
    plt.show()