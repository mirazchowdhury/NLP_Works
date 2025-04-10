def sumOfList(lst):
    lenOfList = len(lst)

    if lenOfList == 0:
        return 0
    else: 
        return lst[0] + sumOfList(lst[1:])
    
print(sumOfList([1,2,3,4,5]))  
    
















lst = [1,2,3,4,5,6]