"""
Given an array of distinct integers candidates and a target integer target, return a list of all unique combinations of candidates where the chosen numbers sum to target. You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.

The test cases are generated such that the number of unique combinations that sum up to target is less than 150 combinations for the given input.

 

Example 1:

Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
Explanation:
2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
7 is a candidate, and 7 = 7.
These are the only two combinations.
Example 2:

Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]
Example 3:

Input: candidates = [2], target = 1
Output: []
 

Constraints:

1 <= candidates.length <= 30
2 <= candidates[i] <= 40
All elements of candidates are distinct.
1 <= target <= 40


"""
class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        candidates.sort() # Lets keep sorted numbers just in case (LEFT: small, RIGHT: large)
        ans: list[list[int]] = []
        curr: list[int] = []

        # Les pass it an index that indicate where in our candidates array we will iterate over
        def recurse(x: int) -> None:
            if sum(curr) > target: return
            if sum(curr) == target:
                ans.append(curr[:])
                return
            
            for i in range(x, len(candidates)):
                currNum = candidates[i]
                curr.append(currNum) # [2, 2, 2, 2]
                if sum(curr) < target: # We can keep adding the same element
                    recurse(i)
                else:
                    
                    recurse(i + 1) # If not, we can move up to another number
                print("Dead end: ", curr, i)
                curr.pop()
        
        recurse(0)
        return ans
    
    def combinationSumOptimal(self, candidates: list[int], target: int) -> list[list[int]]:
        result = []
        curr = []
        
        def recurse(start: int, curr_sum: int):
            if curr_sum == target:
                # We found a valid match, record and stop
                result.append(curr[:])
                return
            elif curr_sum > target or start == len(candidates):
                return # Stop recursing, our sum will only get larger, there's no point
            
            for i in range(start, len(candidates)):
                num = candidates[i]
                curr.append(num)
                recurse(i, curr_sum + num)
                curr.pop()
                
                #recurse(i + 1, curr_sum)

        
        recurse(0, 0)
        return result

    def combinationSumGreg(self, candidates: list[int], target: int) -> list[list[int]]:
        ans, sol = [], []
        n = len(candidates)

        def recurse(i: int, summ: int):
            if summ == target:
                ans.append(sol[:])
                return
            elif summ > target or i == n:
                return
            
            recurse(i + 1, summ)

            sol.append(candidates[i])
            recurse(i, summ + candidates[i])
            sol.pop()
        
        recurse(0, 0)
        return ans
sol = Solution()

candidates = [2, 3, 6, 7]
target = 7

res = sol.combinationSumGreg(candidates, target)

print("Final res: ", res)