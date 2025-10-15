"""
    I want to test out how the sliding window technique works, this way I can also see when to apply these in coding interviews
    
    PROBLEM:
    
    Given an integer array nums and an integer k, find maximum sum of any contiguous subarray of size k
    [1, 12, -5, -6, 50, 3] k = 4
         t          t  is the largest subarray combination that can happen
"""

# Brute force approach
# Start at the fourth position, and then increase by one the range, sum all the content and then compare at the end
def bruteFindMaxSubarray(nums: list[int], k: int) -> int:
    # [1, 12, -5, -6, 50, 3]
    #  l           r 
    # 2, 51, 42
    maxVal = -1000000
    for i in range(0, len(nums) - k + 1):
        currentSum = 0
        
        for e in range(i, i + k):
            curr = nums[e]
            currentSum += curr
        
        maxVal = max(maxVal, currentSum)
    
    return maxVal

def slidingWindow(nums: list[int], k: int) -> int:
    # This algorithm does a single run first
    maxResult = 0
    
    for i in range(k):
        maxResult += nums[i]
        
    # Then we do our actual iteration using our previous result
    for i in range(k, len(nums)):
        #print(nums[i])
        currentSum = maxResult + nums[i] - nums[i - k]
        maxResult = max(maxResult, currentSum)
    
    return maxResult

input = [1, 12, -5, -6, 50, 3]
k = 4

res = slidingWindow(input, k)
print(f"FINAL RESULT: {res}")
