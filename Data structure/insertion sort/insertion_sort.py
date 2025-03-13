def insertion_sort_algorithm(lst):
    len_lst = len(lst)
    for index in range(1,len_lst):
        key_value = lst[index]
        previous_index = index - 1
        print(f"Index : {index}")

        while previous_index>=0 and key_value<lst[previous_index]:
            print(f"previous index : {previous_index}")
            lst[previous_index+1]=lst[previous_index]
            previous_index -=1
        lst[previous_index+1] = key_value
        print(key_value)
    return lst

lst = [22,12,15,3,4]
lst = insertion_sort_algorithm(lst)
print(lst) 