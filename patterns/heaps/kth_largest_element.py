"""
Given an integer array nums and an integer k, return the kth largest element in the array.

Note that it is the kth largest element in the sorted order, not the kth distinct element.

Can you solve it without sorting?

 

Example 1:

Input: nums = [3,2,1,5,6,4], k = 2
Output: 5
Example 2:

Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4

"""
import heapq
class Solution:
    def findKthLargest(self, nums: list[int], k) -> int:
        for i in range(len(nums)):
            nums[i] = -nums[i]
        heapq.heapify(nums)

        # Pop the k -1 largest
        for _ in range(k - 1):
            heapq.heappop(nums)
        
        # Return the kth largest
        return -heapq.heappop(nums)


sol = Solution()
inputData = [3,2,1,5,6,4]
k = 2

res = sol.findKthLargest(inputData, k)
print(res)