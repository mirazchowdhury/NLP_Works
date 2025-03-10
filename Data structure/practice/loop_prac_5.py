
def runningSum(nums):
    sum = 0
    runningSumLst = []
    for num in nums:
        sum = sum + num
        runningSumLst.append(sum)
    return runningSumLst

print(runningSum([1,1,1,1]))

