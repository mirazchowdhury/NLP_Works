# def printAllNumbers(minNum):
#     #base case
#     if minNum>50:
#         return
    
#     print(minNum, end=" ")
#     #Recursive case
#     printAllNumbers(minNum+1)

# printAllNumbers(1)

def printAllNumbers(minNum):
    #base case
    if minNum>5:
        return
    
    
    #Recursive case
    printAllNumbers(minNum+1)
    print(minNum, end=" ")

printAllNumbers(1)