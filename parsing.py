# Author : Pratik
# Title  : Data Structure Formation
# Purpose  : Creating Suitable Data Structure from the user input string


def parsing(input_string):
#parsing starts

    EdgeList = list()
    VarList = dict()  
    tuple_list = input_string.replace('(',' ').replace(')',' ').replace(';',' ').split();  # return a list of edges in string format

    for single_tuple_string in tuple_list:
        single_tuple= single_tuple_string.split(',')
        temp_list   = [int(single_tuple[0].split('->')[0]),int(single_tuple[0].split('->')[1])]
        EdgeList.append(temp_list)
        VarList['u'+str(temp_list[0]) + str(temp_list[1])] = int(single_tuple[1])
        VarList['c'+str(temp_list[0]) + str(temp_list[1])]  = int(single_tuple[2])
        
    return [EdgeList,VarList]