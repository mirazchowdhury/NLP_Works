# n =int(input())
# loop_list = []

# for i in range(1,n+1):
#     if(i>=4 and i<n):
#         j =4
#         #print(4)
#         loop_list.append(j)
#     elif(i==n):
#         loop_list.append(5)
#     else:
#         #print(i)
#         loop_list.append(i)

# print(loop_list)

n = int(input())  
loop_list = []  

for i in range(1, n + 1):  
    if n == 1:  
        loop_list.append(1)  
    elif n == 2:  
        loop_list.append(i)  
    elif n == 3:  
        loop_list.append(i)  
    elif i >= 4 and i < n:  
        loop_list.append(4)  
    elif i == n:  
        loop_list.append(5)  
    else:  
        loop_list.append(i)  

print(loop_list)
