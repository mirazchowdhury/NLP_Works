numOfTestcases = int(input())

for value in range(numOfTestcases):
    numOfChocolates = int(input())
    if numOfChocolates%2 == 0:
        print("Yes")
    else:
        print("No")