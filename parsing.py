# Author : Pratik
# Title  : Data Structure Formation
# Purpose  : Creating Suitable Data Structure from the user input string

input_string = "(0->3,10,5);(0->1,10,5);(1->2,10,5);(3->4,10,5);(4->5,10,5);(2->5,10,5);(5->8,10,5);(8->6,-10,5);(6->4,-30,5)(7->6,10,5);(4->7,10,5)"

def parsing(input_string):
#parsing starts

    EdgeList = list()
    VarList = dict()  
    tuple_list = input_string.replace('(',' ').replace(')',' ').replace(';',' ').split();  # return a list of edges in string format

    for single_tuple_string in tuple_list:
        single_tuple= single_tuple_string.split(',')
        temp_list   = [int(single_tuple[0].split('->')[0]),int(single_tuple[0].split('->')[1])]
        EdgeList.append(temp_list)
        VarList['cost'+str(temp_list[0]) + str(temp_list[1])] = int(single_tuple[1])
        VarList['cap'+str(temp_list[0]) + str(temp_list[1])]  = int(single_tuple[2])
		VarList['flow'+str(temp_list[0]) + str(temp_list[1])]  = 0
    return [EdgeList,VarList]