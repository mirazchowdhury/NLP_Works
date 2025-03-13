def linear_search(lst,value):
    for num in lst:
        if num == value:
            return True
    return False


lst = [1,2,3,4,5]
value = 5
print(linear_search(lst,value))