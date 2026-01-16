"""
Given an integer array nums that may contain duplicates, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.

 

Example 1:

Input: nums = [1,2,2]
Output: [[],[1],[1,2],[1,2,2],[2],[2,2]]
Example 2:

Input: nums = [0]
Output: [[],[0]]
 
"""
class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        finalAns = []
        currSubset = []

        def backtrack(idx: int):
            # When we reach out base case, what do we do?
            if idx == n:
                print('before sort: ', currSubset)
                
                uniqueSubset = sorted(currSubset)
                print('after sort: ', currSubset)
                if uniqueSubset not in finalAns:
                    finalAns.append(uniqueSubset[:])
                return
            
            # Left side (DONT INCLUDE NUMBER)
            backtrack(idx + 1)

            # Right side (INCLUDE NUMBER)
            currSubset.append(nums[idx])
            backtrack(idx + 1)

            # Backtrack
            currSubset.pop()
        
        backtrack(0)
        return finalAns
    def subsets2(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        finalArr, currSubset = [], []
        
        def backtrack(idx: int):
            # Add current subset at every node, not just leaves
            finalArr.append(currSubset[:])

            for i in range(idx, len(nums)):
                if idx < i and nums[i] == nums[i - 1]: # Then there's a duplicate
                    continue
                currSubset.append(nums[i])
                backtrack(i + 1)
                currSubset.pop()
    
        backtrack(0)
        return finalArr

    def subsets3(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        res = list()
        numsLen = len(nums)
        def back(cur, pos):
            res.append(cur.copy())
            prev = -11
            for i in range(pos, numsLen):
                if prev == nums[i]:
                    continue
                cur.append(nums[i])
                back(cur, i + 1)
                cur.pop()
                prev = nums[i]
        back(list(), 0)
        return res
problem = Solution()
inputData = [4, 1, 0]

res = problem.subsets3(inputData)

print(res)

