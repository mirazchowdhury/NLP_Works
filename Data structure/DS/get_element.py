# numbers = [5, 7, 11, 15]
# target_sum = 16

# # Finding pairs that sum to target_sum
# result = []
# for i in range(len(numbers)):
#     for j in range(i + 1, len(numbers)):
#         if numbers[i] + numbers[j] == target_sum:
#             result.append([i, j])


# print(result)



def find_target_sum_pairs(numbers, target_sum):
    result = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target_sum:
                result.append(([numbers[i], numbers[j]], [i, j]))
    return result

numbers = [2, 7, 11, 15]
target_sum = 26
print(find_target_sum_pairs(numbers, target_sum))
