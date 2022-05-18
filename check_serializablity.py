# Advanced DataBase Final project 1401
# Shahid Beheshti University 
# Course Presenter : Dr Haghighi
# Author : Arash Alam 
# Student Id :400443146
# Date Project Done -> 19 MAY 2022 or 29 Ordibehesht 1401
__author__ = "Arash Alam"
from itertools import permutations
# permutations using library function
# data we use in transactions : (key = data_name) & (value = data) 
datas = {}
datas_copy = {}

# we need this
# no_of_transactions = 0

# we need this list to add data info to dict
operation_list= []
new_operation_list = []
temp_ls = []
temp_ls_final = []
my_data = []
flg = True
check_list = []
check_list2 = []

view_list = []
# line number initial number 
line_number = 0

# this temp will be use to transform data
temp = ""

no_of_transactions = 0
no_of_transactions_list = []
permutate_trans_list = []    
print("\n")
    
check_conflict_list = []

# read input.txt file
with open('./input4.txt') as f:
    lines = f.readlines()
# line_numbers of txt file
line_number = len(lines)
    
    
# Get all permutations of transaction can run serial
def permutate():
    perm = permutations(no_of_transactions_list)
    global permutate_trans_list
    for i in list(perm):
        permutate_trans_list.append(list(i))
    # print("\n") 
    # print(f"The all permutation list of transactions are : \n {permutate_trans_list}")
    # print("\n") 
    
    
# here we extract data we need and transactions use that come after '#' sign at first lines  
def extract_data():
    for line in lines:
        flag = 0
        mylist = []
        mylist.clear()
        temp = ""
        line = line.replace(" ","")
                    
        if line[0]=='#':
            if line[1].isupper()==True:
                print(f"Input Error : Data names must be lower case --> {line[1]} must be {line[1].lower()}, check input file")
                flag = 1
                break                
            elif line[1] == '=':
                print("Input Error : No Data name after # , check input file")
                flag = 1
                break                
            elif line[2] != '=':
                print(f"Input Error : Data name must be one char from a to z so.")
                flag = 1
                break                
            else:
                temp = line[1:]
                temp = temp.strip()
                mylist = temp.split("=")
                if int(mylist[1]) < 0 :
                    print("Input Error : Data values must be > 0 (Integer Positive).")
                    flag = 1
                    break                
                elif int(mylist[1]) > 0:
                    datas[mylist[0]] = mylist[1]
                    
    for key in datas.keys():
        my_data.append(key)
    for key in datas:
        datas[key] = int(datas[key])                         
    if flag == 0:
        print("===============================================================")
        print("The data and values transactions use are : \n", datas)
        print("===============================================================")
        print("The data transactions use are : \n", my_data)
        print("===============================================================") 
        operation_transaction()                 
    elif flag == 1:
        print("\n")

       

# here we extract operations used in transactions <line , Transaction no , operation> and put them in operation_list  
def operation_transaction():    
    for line in lines:
        flag = 0
        line = line.strip()
        temp = ""
        line = line.replace(" ","")
        if line[0] == '#' and line[-1] != '>':
            continue;
        elif line[0]!='<':
           flag = 1
           print(f"Input Error : The transaction info format must start with '<' not {line[0]}.")
           break 
        elif line[-1] != '>':
            flag = 1
            print(f"Input Error : The transaction info format must end with '>' not '{line[-1]}' .")
            break 
        elif line[0]=='<' and line[-1]=='>':
            line = line.replace("<","")
            line = line.replace(">","")
            line = line.strip()
            operation_list.append(line.split(","))
            
            
                
    if flag == 0:   
        print("The line numbers, transactions number, operation used are : \n", operation_list)                
        print("\n")
        transaction_numbers()
    elif flag == 1:
        print("\n")


# here we are going to calculate number of transactions in shedule
def transaction_numbers():
    global no_of_transactions
    global no_of_transactions_list
    for i in range(len(operation_list)):
        if int(operation_list[i][1]) == no_of_transactions + 1:
           no_of_transactions += 1
           no_of_transactions_list.append(no_of_transactions)
    global trans_lines 
    trans_lines = {}
    for i in range(1, no_of_transactions+1):
        trans_lines[str(i)] = []
    x = list(trans_lines.keys())
    for i in range(len(operation_list)):
        for item in range(len(x)):    
            if (x[item] == operation_list[i][1]):
                trans_lines[f'{x[item]}'].append(operation_list[i])
            
    global trans_list
    trans_list = [[] for _ in range(no_of_transactions)]    
    # global trans_list2
    # trans_list2 = [[] for _ in range(no_of_transactions)]    
    
    # print(trans_list)
    print("The transactions number is : ", no_of_transactions)
    print("\n")
    permutate()
    check_conflict(operation_list)

    # print("The transactions number in list : \n", no_of_transactions_list)
    # print("\n")
    # print("The transactions lines in list : \n", trans_lines)
    

# here we check conflict serializability
def check_conflict(operation_list):
    flag = False
    temp_list = []
    for i in range(len(operation_list)):
        temp_list = []
        the_char = operation_list[i][2][0]
        the_data = operation_list[i][2][2]
        if the_char != 'R' and the_char != 'W' :
            continue
        elif the_char == 'R' or the_char == 'W' :
            temp_list.append(operation_list[i][0])
            temp_list.append(operation_list[i][1])
            temp_list.append(the_char)
            temp_list.append(the_data)
#the next line is the list we use to figure out if thers is a conflict or not. 
            new_operation_list.append(temp_list)
    
    for i in range(len(new_operation_list)):
        # no need to check first index
        temp_list = []
        
        if i == 0: 
            continue
        
        else:
            
            for j in range(len(new_operation_list)):
                
                if j >= i:
                    break
                    
                    
                elif j < i :
                #    check if operations are not conflict and both of them are :  Read & Read
                    if new_operation_list[i][2] == 'R' and new_operation_list[j][2] == 'R':
                   
                        continue
                   
                    else:
                        # check if trans are the same
                        if new_operation_list[i][1] == new_operation_list[j][1]:
                            continue
                        else:
                            # check if the conflict is on same data.
                            if new_operation_list[i][3] != new_operation_list[j][3]:
                                continue
                            else:
                                for k in range(len(new_operation_list)):
                                    if k <= i :
                                        continue
                                    else:
                                        # check the before and after trans(i) conflicts are the same 
                                        if new_operation_list[j][1] == new_operation_list[k][1]:
                                            if new_operation_list[i][2] == 'R' and new_operation_list[k][2] == 'R':
                                                continue
                                            else:
                                                if new_operation_list[i][3] != new_operation_list[k][3]:
                                                    continue
                                                else:
                                                    print("===============================================================")
                                                    print("Conflict Serialiazability : NO \n")
                                                    print("Because there is no serial schedule to solve below conflict: \n")
                                                    print(f"Line : {new_operation_list[j][0]} ,Transaction : {new_operation_list[j][1]} , operation : {new_operation_list[j][2]} , data : {new_operation_list[j][3]} \n")
                                                    print(f"Line : {new_operation_list[i][0]} ,Transaction : {new_operation_list[i][1]} , operation : {new_operation_list[i][2]} , data : {new_operation_list[i][3]} \n")
                                                    print(f"Line : {new_operation_list[k][0]} ,Transaction : {new_operation_list[k][1]} , operation : {new_operation_list[k][2]} , data : {new_operation_list[k][3]} \n")
                                                    print("===============================================================")
                                                    check_view(new_operation_list)
                                                    show_view_result(view_flag)
                                                    return
                                                
    for i in range(len(new_operation_list)):
        flg = True
        for j in range(len(new_operation_list)):
            if flg == False:
                break
            else:
                if int(new_operation_list[j][0]) == int(new_operation_list[i][0]):
                    continue
                else:
                    if int(new_operation_list[i][1]) == int(new_operation_list[j][1]):
                        continue
                    else:
                        if new_operation_list[i][2] == 'R' and new_operation_list[j][2] == new_operation_list[i][2]:
                            continue
                        else:
                            if new_operation_list[i][3] == new_operation_list[j][3] :
                                for item in range(len(my_data)):
                                    if new_operation_list[i][3] == my_data[item]:
                                        del my_data[item]
                                        check_list.append(new_operation_list[i][1])
                                        flg = False
                                        break
                                    else:
                                        continue
    # print(check_list)
    if len(check_list) > 0:    
        check_list2.append(check_list[0])
        for i in range(len(check_list)):
            for j in range(len(check_list2)):
                if check_list[i] == check_list2[j]:
                    break
                elif (j != len(check_list2) - 1):
                    continue
                else:   
                    check_list2.append(check_list[i])
                    break
    # print(check_list2)
    print("\n")            
    if len(my_data) == 0 and len(check_list2) > 1 :
        print("===============================================================")
        print("Conflict Serialiazability : NO \n")
        print("Because there is no serial schedule to solve conflict. \n")
        print("===============================================================")
        check_view(new_operation_list)
        show_view_result(view_flag)                                
        return
    else : 
        flag = True;                                                
                                        
                    
        
    if flag == True:
        print("===============================================================")
        print("Conflict Serialiazablity : YES \n")                                        
        #print(new_operation_list)
        for i in range(len(new_operation_list)):
            for j in range(len(new_operation_list)):
                if int(new_operation_list[i][0]) >= int(new_operation_list[j][0]):
                    continue
                elif int(new_operation_list[i][1]) == int(new_operation_list[j][1]):
                    temp_ls.append(new_operation_list[i][1])
                    continue
                elif new_operation_list[i][2] == 'R' and new_operation_list[j][2] == 'R':
                    temp_ls.append(new_operation_list[i][1])
                    continue
                else:   
                    for k in range(len(temp_ls)):
                        if new_operation_list[i][1] != temp_ls[k] and new_operation_list[j][1] != temp_ls[k]:
                            temp_ls.append(operation_list[i][1])
                            temp_ls.append(operation_list[j][1])   
                                 
                    # else:
                        # continue
        # print(temp_ls)
        temp_ls_final.append(temp_ls[0])
        for i in range(len(temp_ls)):
            for j in range(len(temp_ls_final)):
                if temp_ls[i] == temp_ls_final[j]:
                    break
                elif (j != len(temp_ls_final) - 1):
                    continue
                else:   
                    temp_ls_final.append(temp_ls[i])
                    break

    # print(temp_ls_final)
        str = ""
        for item in range(len(temp_ls_final)):
            if (item != len(temp_ls_final) - 1):
                str += "T" + temp_ls_final[item] +" -> "
            else:
                str += "T" +temp_ls_final[item] + " . "
                break            
        print("Equivalence to this serialiazable schedule : " + str)
        print("===============================================================")
        print("View Serialiazablity : YES \n")                                        
        print("===============================================================")
        print("Result Serialiazablity : YES \n")
        print("===============================================================")
        
    
                                                                                            
# get the variable new_operation_list from line 226
def check_view(operation):
    view_list = []
    global view_flag
    view_flag = False
    for i in range(len(operation)):
        if operation[i][2] == 'W':
            for j in range(len(operation)):
                if operation[j][2] == 'R' and int(operation[j][1]) == int(operation[i][1]) and operation[j][3] == operation[i][3] and int(operation[i][0]) > int(operation[j][0]):
                    break
                elif int(operation[i][0]) > int(operation[j][0]):
                    continue
                elif int(operation[i][0]) == int(operation[j][0]):
                    view_flag = True
                    return                      
                                                     
                            
                        
                  
                                                    
def check_result(res_flag):
    
    if res_flag == True:
    
        print("Result Serializability : YES \n ")
        print("===============================================================")
    
    else:
        final_flg = False
        datas_copy = datas.copy()
        
        for i in range(len(operation_list)):
            
            if operation_list[i][2][0] == 'R':
                # trans_list[int(operation_list[i][1]) - 1].append(operation_list[i][2][0])         
                continue
                # print(trans_list)       
            
            elif operation_list[i][2][0] == 'W':
                wrt_flag = True
                for j in range(len(operation_list)):
                    if wrt_flag == True:
                        
                        # for j in range(len(operation_list)):
                            
                            if j < i and wrt_flag == True and operation_list[j][2][0] == 'R' and operation_list[i][2][2] == operation_list[j][2][2] and int(operation_list[j][1]) == int(operation_list[i][1]):
                                
                                for item in trans_list:
                                    for element in item:
                                        index = trans_list.index(item)
                                        if element == operation_list[i][2][2] and index == (int(operation_list[i][1]) -1):
                                            index2 = item.index(element)
                                            # print(item[index2+1])
                                            datas_copy[operation_list[i][2][2]] = item[index2+1]
                                            wrt_flag = True
                            elif j < i:
                            
                                continue
                            
                            else:
                                wrt_flag = False
                                break                                                
                    else:
                        break                
                    
            else:
                
                if operation_list[i][2][0] in datas_copy.keys() :
                
                    if operation_list[i][2][1] == '=':
                        
                        trans_list[int(operation_list[i][1]) - 1].append(operation_list[i][2][0])
                        # print(trans_list)
                        if operation_list[i][2][3] == '/':
                        
                                                   
                            if operation_list[i][2][2] in datas_copy.keys():
                                if operation_list[i][2][4] in datas_copy.keys():
                                    temp_data = datas_copy[operation_list[i][2][2]] / datas_copy[operation_list[i][2][4]]            
                                    trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                
                                else:
                                    tmp = int(operation_list[i][2][4:])
                                    temp_data = datas_copy[operation_list[i][2][2]] / tmp            
                                    trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                                                                
                            elif operation_list[i][2][4] in datas_copy.keys():
                               tmp = int(operation_list[i][2][2:])
                               temp_data = tmp / datas_copy[operation_list[i][2][4]]
                               trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                
                            else:
                                 tmp1 = int(operation_list[i][2][2:])    
                                 tmp2 = int(operation_list[i][2][4:])    
                                 temp_data = tmp1 / tmp2            
                                 trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                
                        
                        
                        elif operation_list[i][2][3] == '*':
                            
                            if operation_list[i][2][2] in datas_copy.keys():
                                if operation_list[i][2][4] in datas_copy.keys():
                                    temp_data = datas_copy[operation_list[i][2][2]] * datas_copy[operation_list[i][2][4]]            
                                    trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                
                                else:
                                    tmp = int(operation_list[i][2][4:])
                                    temp_data = datas_copy[operation_list[i][2][2]] * tmp            
                                    trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                                                                
                            elif operation_list[i][2][4] in datas_copy.keys():
                               tmp = int(operation_list[i][2][2:])
                               temp_data = tmp * datas_copy[operation_list[i][2][4]]
                               trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                
                            else:
                                 tmp1 = int(operation_list[i][2][2:])    
                                 tmp2 = int(operation_list[i][2][4:])    
                                 temp_data = tmp1 * tmp2            
                                 trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                
                
                
                        
                            
                        elif operation_list[i][2][3] == '-':
                        
                        
                            if operation_list[i][2][2] in datas_copy.keys():
                                if operation_list[i][2][4] in datas_copy.keys():
                                    temp_data = datas_copy[operation_list[i][2][2]] - datas_copy[operation_list[i][2][4]]            
                                    trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                
                                else:
                                    tmp = int(operation_list[i][2][4:])
                                    temp_data = datas_copy[operation_list[i][2][2]] - tmp            
                                    trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                                                                
                            elif operation_list[i][2][4] in datas_copy.keys():
                               tmp = int(operation_list[i][2][2:])
                               temp_data = tmp - datas_copy[operation_list[i][2][4]]
                               trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                
                            else:
                                 tmp1 = int(operation_list[i][2][2:])    
                                 tmp2 = int(operation_list[i][2][4:])    
                                 temp_data = tmp1 - tmp2            
                                 trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                
                
                
                        
                        
                        elif operation_list[i][2][3] == '+':
                        
                            
                            if operation_list[i][2][2] in datas_copy.keys():
                                if operation_list[i][2][4] in datas_copy.keys():
                                    temp_data = datas_copy[operation_list[i][2][2]] + datas_copy[operation_list[i][2][4]]            
                                    trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                
                                else:
                                    tmp = int(operation_list[i][2][4:])
                                    temp_data = datas_copy[operation_list[i][2][2]] + tmp            
                                    trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                                                                
                            elif operation_list[i][2][4] in datas_copy.keys():
                               tmp = int(operation_list[i][2][2:])
                               temp_data = tmp + datas_copy[operation_list[i][2][4]]
                               trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                
                            else:
                                 tmp1 = int(operation_list[i][2][2:])    
                                 tmp2 = int(operation_list[i][2][4:])    
                                 temp_data = tmp1 + tmp2            
                                 trans_list[int(operation_list[i][1]) - 1].append(temp_data)
                
                
                        
                        else:
                            print("there is a error.")    

        print("The result of current schedule is : \n")                            
        print(datas_copy)                                   
        
        for item in range(len(operation_list)):
            operation_list[item][0] = int(operation_list[item][0])
            operation_list[item][1] = int(operation_list[item][1])
        for k in range(len(permutate_trans_list)):
            tmp_lis = []
            trans_list2 = [[] for _ in range(no_of_transactions)]    

            datas_copy2 = datas.copy()
            for m in range(len(permutate_trans_list[k])):
               for i in range(len(operation_list)):
                    if operation_list[i][1] == permutate_trans_list[k][m] and final_flg == False:
                       
                        if operation_list[i][2][0] == 'R':
                    
                           continue
                
                        elif operation_list[i][2][0] == 'W':
                
                            wrt_flag = True
                            for j in range(len(operation_list)):
                                if wrt_flag == True:                            
                                    if j < i and wrt_flag == True and operation_list[j][2][0] == 'R' and operation_list[i][2][2] == operation_list[j][2][2] and int(operation_list[j][1]) == int(operation_list[i][1]):
                                
                                        for item in trans_list2:
                                            for element in item:
                                                index = trans_list2.index(item)
                                                if element == operation_list[i][2][2] and index == (int(operation_list[i][1]) -1):
                                                    index2 = item.index(element)
                                            # print(item[index2+1])
                                                    datas_copy2[operation_list[i][2][2]] = item[index2+1]
                                                    wrt_flag = True
                                    elif j < i:            
                                        continue
                            
                                    else:
                                        wrt_flag = False
                                        break                                                
                                else:
                                    break
                        
                        else:
                    
                            if operation_list[i][2][0] in datas_copy2.keys() :
                            
                                if operation_list[i][2][1] == '=':
                                    
                                    trans_list2[int(operation_list[i][1]) - 1].append(operation_list[i][2][0])
                                    # print(trans_list2)
                                    if operation_list[i][2][3] == '/':
                                    
                                                            
                                        if operation_list[i][2][2] in datas_copy2.keys():
                                            if operation_list[i][2][4] in datas_copy2.keys():
                                                temp_data = datas_copy2[operation_list[i][2][2]] / datas_copy2[operation_list[i][2][4]]            
                                                trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                            
                                            else:
                                                tmp = int(operation_list[i][2][4:])
                                                temp_data = datas_copy2[operation_list[i][2][2]] / tmp            
                                                trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                                                                            
                                        elif operation_list[i][2][4] in datas_copy2.keys():
                                            tmp = int(operation_list[i][2][2:])
                                            temp_data = tmp / datas_copy2[operation_list[i][2][4]]
                                            trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                                
                                        else:
                                            tmp1 = int(operation_list[i][2][2:])    
                                            tmp2 = int(operation_list[i][2][4:])    
                                            temp_data = tmp1 / tmp2            
                                            trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                            
                                    
                                    
                                    elif operation_list[i][2][3] == '*':
                                        
                                        if operation_list[i][2][2] in datas_copy2.keys():
                                            if operation_list[i][2][4] in datas_copy2.keys():
                                                temp_data = datas_copy2[operation_list[i][2][2]] * datas_copy2[operation_list[i][2][4]]            
                                                trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                            
                                            else:
                                                tmp = int(operation_list[i][2][4:])
                                                temp_data = datas_copy2[operation_list[i][2][2]] * tmp            
                                                trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                                                                            
                                        elif operation_list[i][2][4] in datas_copy2.keys():
                                            tmp = int(operation_list[i][2][2:])
                                            temp_data = tmp * datas_copy2[operation_list[i][2][4]]
                                            trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                                
                                        else:
                                            tmp1 = int(operation_list[i][2][2:])    
                                            tmp2 = int(operation_list[i][2][4:])    
                                            temp_data = tmp1 * tmp2            
                                            trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                            
                            
                            
                                    
                                        
                                    elif operation_list[i][2][3] == '-':
                                    
                                    
                                        if operation_list[i][2][2] in datas_copy2.keys():
                                            if operation_list[i][2][4] in datas_copy2.keys():
                                                temp_data = datas_copy2[operation_list[i][2][2]] - datas_copy2[operation_list[i][2][4]]            
                                                trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                            
                                            else:
                                                tmp = int(operation_list[i][2][4:])
                                                temp_data = datas_copy2[operation_list[i][2][2]] - tmp            
                                                trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                                                                            
                                        elif operation_list[i][2][4] in datas_copy2.keys():
                                            tmp = int(operation_list[i][2][2:])
                                            temp_data = tmp - datas_copy2[operation_list[i][2][4]]
                                            trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                            
                                        else:
                                            tmp1 = int(operation_list[i][2][2:])    
                                            tmp2 = int(operation_list[i][2][4:])    
                                            temp_data = tmp1 - tmp2            
                                            trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                            
                            
                            
                                    
                                    
                                    elif operation_list[i][2][3] == '+':
                                    
                                        
                                        if operation_list[i][2][2] in datas_copy2.keys():
                                            if operation_list[i][2][4] in datas_copy2.keys():
                                                temp_data = datas_copy2[operation_list[i][2][2]] + datas_copy2[operation_list[i][2][4]]            
                                                trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                            
                                            else:
                                                tmp = int(operation_list[i][2][4:])
                                                temp_data = datas_copy2[operation_list[i][2][2]] + tmp            
                                                trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                                                                            
                                        elif operation_list[i][2][4] in datas_copy2.keys():
                                            tmp = int(operation_list[i][2][2:])
                                            temp_data = tmp + datas_copy2[operation_list[i][2][4]]
                                            trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                            
                                        else:
                                            tmp1 = int(operation_list[i][2][2:])    
                                            tmp2 = int(operation_list[i][2][4:])    
                                            temp_data = tmp1 + tmp2            
                                            trans_list2[int(operation_list[i][1]) - 1].append(temp_data)
                            
            
                                    else:
                                        print("there is a error.")                
            if m == (len(permutate_trans_list[k]) - 1) and final_flg == False:
                if datas_copy == datas_copy2:
                    print("\n")
                    print("Result Serialiazability : YES \n")
                    print("And equivalent to this schedule : \n")
                    for item in range(len(permutate_trans_list[k])):
                        print(f"T{permutate_trans_list[k][item]} \n")
                        final_flg = True
                    print("===============================================================")    
                elif final_flg == True:
                    break                 
            elif len(permutate_trans_list) - 1 == k and final_flg == False:
                print("\n")
                print("Result Serialiazability : NO \n")
            else: 
                continue    
                                                    
            
        
        

def show_view_result(view_flg):
    global temp_li
    temp_li= []
    if view_flg == False:
        print("View Serialiazability : NO \n")
        print("===============================================================")
        check_result(view_flag)
    else:
        print("View Serialiazability : YES \n")
        for i in range(len(new_operation_list)):
            if new_operation_list[i][2] == 'R':
                if len(temp_li) == 0 :
                    temp_li.append(new_operation_list[i][1])
                else:
                    for item in range(len(temp_li)):
                        if temp_li[item] == new_operation_list[i][1]:
                            break
                        elif item != len(temp_li) - 1 :
                            continue
                        else:
                            temp_li.append(new_operation_list[i][1])
            else:
                
                if i == len(new_operation_list) - 1 :
                    if len(temp_li) == 0 :
                            temp_li.append(new_operation_list[i][1])
                    else:
                        for item in range(len(new_operation_list)):
                            if temp_li[item] == new_operation_list[i][1]:
                                break
                            elif item != len(temp_li) - 1 :
                                continue
                            else:
                                temp_li.append(new_operation_list[i][1])
                                break
                else:     
                    
                    for j in range(len(new_operation_list)):
                        if new_operation_list[i][0] >= new_operation_list[j][0] :
                            continue
                        elif new_operation_list[i][0] < new_operation_list[j][0]:
                            if new_operation_list[i][3] != new_operation_list[j][3]:
                                continue
                            else:
                                if new_operation_list[j][2] != new_operation_list[i][2]:
                                    continue
                                else:
                                    if len(temp_li) == 0 :
                                        temp_li.append(new_operation_list[i][1])
                                    else:
                                        for item in range(len(new_operation_list)):
                                            if temp_li[item] == new_operation_list[i][1]:
                                                break
                                            elif item != len(temp_li) - 1 :
                                                continue
                                            else:
                                                temp_li.append(new_operation_list[i][1])
                                                break
                            
        str = ""
        for item in range(len(temp_li)):
            if (item != len(temp_li) - 1):
                str += "T" + temp_li[item] +" -> "
            else:
                str += "T" +temp_li[item] + " . "
                break
        print("Equivalence to this serialiazable schedule : " + str )
        print("===============================================================")
        check_result(view_flag)
                
#Here where i call methods to run 
extract_data()
# operation_transaction() 
# transaction_numbers()
# permutate()
# check_conflict(operation_list)
# check_result_serializability()
# print(permutate_trans_list)

