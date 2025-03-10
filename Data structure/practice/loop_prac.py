# n = int(input("Type any number : "))
# for i in range(1,n):
#     if i%10 == 0:
#         print(i)
#         i += 1
#     elif i>150:
#         break

# n = int(input("Type any number: "))
# output_list = []  # Initialize an empty list

# for i in range(1, n):
#     if i % 10 == 0:
#         output_list.append(i)  # Store the value in the list
#         i += 1
#     elif i > 150:
#         break

# print("Output List:", output_list)  # Print the list after the loop


numOfElements = int(input())
lst = []

for value in range(numOfElements):
    num = int(input())
    lst.append(num)

for num in lst:
    if num<=120:
        if num%10 == 0:
            print(num)
    else:
        break




