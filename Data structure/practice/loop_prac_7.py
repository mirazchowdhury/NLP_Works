numOfTestcases = int(input())

for value in range(numOfTestcases):
    num = int(input())
    if num == 0:
        print("Null")
    elif num>0:
        if num%2 == 0:
            print("Even Positive")
        else:
            print("Odd Positive")
    else:
        if num%2 == 0:
            print("Even Negative")
        else:
            print("Odd Negative")