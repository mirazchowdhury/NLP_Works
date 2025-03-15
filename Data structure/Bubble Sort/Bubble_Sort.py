def Bubble_Sort(lst):
    len_of_list = len(lst) #6
    for outer_index in range(len_of_list):
        range_of_inner_loop = len_of_list - outer_index - 1  #or, len_of_list - 1
        for inner_index in range(range_of_inner_loop):
            print(f"Outer index : {outer_index} and inner index : {inner_index}")
            if lst[inner_index] > lst[inner_index+1]:
                temp = lst[inner_index]
                lst[inner_index] = lst[inner_index+1]
                lst[inner_index+1] = temp
            print(lst)




lst = [-90,-10,-1000,1300,18,0]
Bubble_Sort(lst)

print(lst)