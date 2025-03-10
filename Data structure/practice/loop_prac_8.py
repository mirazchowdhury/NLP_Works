def singleNumber(nums):
    result = 0   # Start with 0 because XOR with 0 gives the same number.
    for num in nums:
        result ^= num  # XOR each number with result
    return result  # The remaining number is the answer

print(singleNumber([4,1,2,1,2]))  # Output: 4
