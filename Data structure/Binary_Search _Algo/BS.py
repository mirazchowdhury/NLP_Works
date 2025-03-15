lst = [10,20,30,40,50]
targetValue = 40

start = 0 

end = len(lst) 


while start <= end: 
    mid =  (start + end) // 2 
    print(f"Start : {start}, End: {end}, mid: {mid}, lst[mid] : {lst[mid]}")
    if lst[mid] == targetValue: 
        print("Value Exists")
        break
    elif lst[mid] < targetValue: 
        start = mid + 1 
    elif lst[mid] > targetValue: 
        end  = mid - 1

    
