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
        
        #print(pArr)
        return pArr
    
    
solution = PrefixSum()

inputData = [8, 3, -2, 4, 10, -1, 0, 5, 3]
# res = [0, 8, 11, 9, 13, 23, 22, 22, 27, 30]

res = solution.prefixSum(inputData)
print(res)
print(f"Range given: {res[3] - res[0]}")

# Formula: pArr[i] = p[i - 1] + a[i]