"""
    🔹 Problem 1: Product of Array

Given an array of integers arr, return the product of all elements.
Example: [2, 3, 4] → 24

Hint:

Base case → empty list (or list of size 1).

Recursive step → multiply the first element with the product of the rest.
"""

class Recursion:
    def productOfArr(self, nums: int) -> int:
        # base case
        if len(nums) <= 1:
            return nums[0]
        
        currentNum = nums[-1]
        restNums = nums[: -1]
        
        return currentNum * self.productOfArr(restNums)
    

inputData = [2, 3 ,4]
solutionInstance = Recursion()
res = solutionInstance.productOfArr(inputData)

print(res)