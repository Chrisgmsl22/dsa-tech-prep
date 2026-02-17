"""
    Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.

Example 1:

Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
Example 2:

Input: nums = [0,1]
Output: [[0,1],[1,0]]
Example 3:

Input: nums = [1]
Output: [[1]]
 

"""

class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        allPermutations = []
        currPermutation = []
        mySet = set()

        def dfs():
            if len(currPermutation) == len(nums):
                allPermutations.append(currPermutation[:])
                return
            
            for num in nums:
                if num not in mySet:
                    # Then we will append, recurse and backtrack
                    currPermutation.append(num)
                    mySet.add(num)
                    dfs()
                    currPermutation.pop()
                    mySet.remove(num)
        
        
        dfs()
        return allPermutations



nums = [1, 2, 3]
sol = Solution()
res = sol.permute(nums)

print("Final solution: ", res)