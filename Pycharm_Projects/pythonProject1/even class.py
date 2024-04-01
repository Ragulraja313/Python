class Solution:
    a = 0

    def twoSum(self, a):
        self.a = a
        if a % 2 == 0:
            print("Even")
        else:
            print("Odd")


obj = Solution()
obj.twoSum(int(input()))
