# def balancedStringSplit(s):
#     count = 0  # Tracks the balance between 'L' and 'R'
#     max_splits = 0  # Stores the number of balanced substrings
    
#     for char in s:
#         if char == 'L':
#             count += 1
#         else:
#             count -= 1
        
#         if count == 0:
#             max_splits += 1  # Found a balanced substring
    
#     return max_splits

# # Example test cases
# print(balancedStringSplit("RLRRLLRLRL"))  # Output: 4
# print(balancedStringSplit("RLRRRLLRLL"))  # Output: 2
# print(balancedStringSplit("LLLLRRRR"))    # Output: 1

def balancedStringSplit(s):
    r_count = 0
    l_count = 0
    pair_count = 0

    for ch in s:
        if ch == "R":
            r_count = r_count+1
        elif ch == "L":
            l_count = l_count+1

        if r_count == l_count:
            pair_count = pair_count+1

    return pair_count

print(balancedStringSplit("RLRRLLRLRL"))
print(balancedStringSplit("RLRRRLLRLL"))
print(balancedStringSplit("LLLLRRRR"))