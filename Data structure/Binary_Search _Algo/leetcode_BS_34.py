class Solution(object):
    def searchRange(self, nums, target):
        len_of_nums = len(nums)
        start, end = 0, len_of_nums - 1
        isExist = self.search(nums, target)

        if isExist is not False:  # 0 ইনডেক্সও true ধরবে
            first, last = -1, -1

            # প্রথম অবস্থান খোঁজা
            for i in range(len_of_nums):
                if nums[i] == target:
                    first = i
                    break  # প্রথম পাওয়া মাত্র ব্রেক করব

            # শেষ অবস্থান খোঁজা
            for i in range(len_of_nums - 1, -1, -1):
                if nums[i] == target:
                    last = i
                    break  # শেষ পাওয়া মাত্র ব্রেক করব

            return [first, last]

        return [-1, -1]

    def search(self, nums, target):
        start, end = 0, len(nums) - 1

        while start <= end:
            mid = (start + end) // 2
            if nums[mid] == target:
                return mid  # টার্গেট পাওয়া গেলে ইনডেক্স রিটার্ন করব
            elif nums[mid] < target:
                start = mid + 1
            else:
                end = mid - 1
        return False  # টার্গেট না থাকলে False রিটার্ন করব


# টেস্ট কেস
solution = Solution()
print(solution.searchRange([1], 1))  # Output: [0, 0]
print(solution.searchRange([5, 7, 7, 8, 8, 10], 8))  # Output: [3, 4]
print(solution.searchRange([1, 2, 3, 4, 5], 6))  # Output: [-1, -1]



# class Solution(object):
#     def searchRange(self,nums,target):
#         len_of_nums = len(nums)
#         start = 0
#         end = len_of_nums - 1
#         isExist = self.search(nums,target)


#         if isExist:
#             for index in range(0,len_of_nums):
#                 if nums[start] == nums[end]:
#                     return[start,end]
#                 elif nums[start]< target:
#                     start +=1
#                 else:
#                     end -=1
#         else:
#             return [-1,-1]
            
#     def search(self,nums,target):
#         start = 0 
#         end = len(nums) - 1


#         while start <= end: 
#             mid =  (start + end) // 2 
            
#             if nums[mid] == target: 
               
#                 return mid
#             elif nums[mid] < target: 
#                 start = mid + 1 
#             elif nums[mid] > target: 
#                 end  = mid - 1
#         return False
