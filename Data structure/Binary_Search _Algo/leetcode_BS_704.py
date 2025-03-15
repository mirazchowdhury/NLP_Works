def search(nums,target):
    start = 0 
    end = len(nums) - 1


    while start <= end: 
        mid =  (start + end) // 2 
        #print(f"Start : {start}, End: {end}, mid: {mid}, nums[mid] : {nums[mid]}")
        if nums[mid] == target: 
            #print("Value Exists")
            #break
            return mid
        elif nums[mid] < target: 
            start = mid + 1 
        elif nums[mid] > target: 
            end  = mid - 1
    return -1 
nums = [10,20,30,40,50]
target = 1
print(search(nums,target))