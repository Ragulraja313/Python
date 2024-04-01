from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int):
        n = len(nums)
        for i in range(n - 1):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [nums[i], nums[j]]
        return []


obj = Solution()
a = obj.twoSum([3, 4, 3], 6)
print(a)