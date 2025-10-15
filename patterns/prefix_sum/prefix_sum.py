"""
    Given an array of integer nums, calculate the sum from a given range
"""

class PrefixSum:
    def __init__(self):
        pass
    
    def prefixSum(self, nums: list[int]) -> list[int]:
        # first, initialize the array to be of size N
        arrSize: int = len(nums)
        pArr = [0] * (arrSize + 1)
        
        for i in range(1, arrSize + 1):
            pArr[i] = pArr[i - 1] + nums[i - 1]
        
        print(pArr)
    
    
solution = PrefixSum()

inputData = [8, 3, -2, 4, 10, -1, 0, 5, 3]

res = solution.prefixSum(inputData)

# Formula: pArr[i] = p[i - 1] + a[i]