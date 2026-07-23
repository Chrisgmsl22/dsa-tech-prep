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


Constraints:

2 <= nums.length <= 105
-30 <= nums[i] <= 30
The input is generated such that answer[i] is guaranteed to fit in a 32-bit integer.


Follow up: Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)
"""
class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        arrResult: list[int] = [0] * n
        arrLeft: list[int] = [0] * n
        arrRight: list[int] = [0] * n
        # [1, 2, 3, 4]
        #     |
        # [1, 1, 0, 0]
        running = 1
        for i in range(n):
            arrLeft[i] = running
            running *= nums[i]

        running = 1
        for i in range(n - 1, -1, -1):
            arrRight[i] = running
            running *= nums[i]
        # Now we combine the answers
        for i in range(n):
            arrResult[i] = arrLeft[i] * arrRight[i]
        print(arrLeft, arrRight)
        return arrResult


sol = Solution()
nums = [1,2,3,4]
res = sol.productExceptSelf(nums)

print("OUTPUT: ", res)

"""
    NOTES:
        - Input: an array of numbers
        - Output: an array of numbers, which represent the total multiplication of their elements without the current number

        Things to consider: my array is at least of size 2, my number can be at most 30. And since we are multiplying all their values, we are guaranteed that the result fits in a 32 bit integer (2^31).

        We definitely need to iterate multiple times.
        We go from left to right, and for each element in the array, we iterate again, collect our compute result but also ignore the current number

        Can we have repeated numbers? YES.
        So we cant simply make sure the numbers are not equal, we might need to take a look at the indicess


        The skip current number isnt a conditional, it is based on the order in which I start the iteration.
        The key here is to know that I am not assining the value at the current position for the CURRENT nums[i], I am assigning what was computed before.

        Once I do this, I then compute the value for the NEXT iteration, which will be used at the next iteration (of course). By the time we reach the end we will not have any slots remaining.

"""
