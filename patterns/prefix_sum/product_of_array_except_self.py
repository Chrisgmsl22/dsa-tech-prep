"""
    Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.

 

    Example 1:

    Input: nums = [1,2,3,4]
    Output: [24,12,8,6]
    Example 2:

    Input: nums = [-1,1,0,-3,3]
    Output: [0,0,9,0,0]
    
"""
class ProductArray:
    def __init__(self):
        pass
    def productOfArrayExceptSelf(self, nums: list[int]) -> list[int]:
        # We need to get all elements from the left BEFORE current i
        # We need to get all elements from the right AFTER current i
        arrSize: int = len(nums)
        leftArr: list[int] = [1] * arrSize
        rightArr: list[int] = [1] * arrSize
        result: list[int] = [1] * arrSize
        print(leftArr, rightArr)
        # [1,2,3,4]
        #.     i
        # [1,1,2,6] => LEFT ARR
        for i in range(1, arrSize):
            # We need to handle both cases in a single run? (let's focus on the left side first)
            leftArr[i] = leftArr[i - 1] * nums[i - 1]
        # [1,2,3,4]
        #.     i2
        # [1,1,4,1] => LEFT ARR
        for i in range(arrSize - 2, -1, -1):
            rightArr[i] = rightArr[i + 1] * nums[i + 1]
        print(leftArr, rightArr)
            
                        
        for i in range(arrSize):
            result[i] = leftArr[i] * rightArr[i]
        print(result)
        return result
    
    
solution = ProductArray()

inputData = [1, 2, 3, 4]
res = solution.productOfArrayExceptSelf(inputData)