def sumOfAllNumbers(lst):
    if len(lst) == 0:
        return 0
    else:
        return lst[0] + sumOfAllNumbers(lst[1:])
    
print(sumOfAllNumbers([1,2,3]))
"""
Round 1:
def sumOfAllNumbers([1,2,3]):
    if len(lst) == 0: #False
        return 0
    else:
        return lst[0] + sumOfAllNumbers(lst[1:])  # 1 + sumOfAllNumbers([2,3]) 

"""
"""
Round 2:
def sumOfAllNumbers([2,3]):
    if len(lst) == 0: #False
        return 0
    else:
        return lst[0] + sumOfAllNumbers(lst[1:])  # 2 + sumOfAllNumbers([3])
"""
"""
Round 3:
def sumOfAllNumbers([3]):
    if len(lst) == 0: #False
        return 0
    else:
        return lst[0] + sumOfAllNumbers(lst[1:])  # 3 + sumOfAllNumbers([]) 
"""
"""
Round 4:
def sumOfAllNumbers([]):
    if len(lst) == 0: #False
        return 0
    else:
        return lst[0] + sumOfAllNumbers(lst[1:])  
"""
"""
Round 4 to Round 3:
def sumOfAllNumbers([3]):
    if len(lst) == 0: #False
        return 0
    else:
        return lst[0] + sumOfAllNumbers(lst[1:])  # 3 + 0 = 3
"""
"""
Round 3 to Round 2:
def sumOfAllNumbers([2,3]):
    if len(lst) == 0: #False
        return 0
    else:
        return lst[0] + sumOfAllNumbers(lst[1:])  # 3 + 2 = 5
"""
"""
Round 2 to Round 1:
def sumOfAllNumbers([1,2,3]):
    if len(lst) == 0: #False
        return 0
    else:
        return lst[0] + sumOfAllNumbers(lst[1:])  # 5 + 1 = 6
"""

