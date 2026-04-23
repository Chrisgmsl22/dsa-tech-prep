"""
Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0 instead.

 

Example 1:

Input: temperatures = [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]
Example 2:

Input: temperatures = [30,40,50,60]
Output: [1,1,1,0]
Example 3:

Input: temperatures = [30,60,90]
Output: [1,1,0]

"""
# Monotonic decreasing stack
class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        # Dont forget edge cases
        n = len(temperatures)
        res = [0] * n
        stk: list[int] = [] # This will store indices, not values, so keep that in mind
        # [73,74,75,71,69,72,76,73]
        #     i
        #                       x           
        # res = [0, 0, 0, 0, 0, 0, 0, 0] remember indices
        # stk = [0]
        for i in range(n):
            currTemp = temperatures[i]
            while stk and temperatures[stk[-1]] < currTemp:
                topIdx = stk.pop()
                res[topIdx] = i - topIdx # Each index position is going to represent a day
                # Keep poppig 
            # If its cold, then add it to our stack to process
            stk.append(i)
        return res


"""
- Input: an array called temperatures, an array of integers
- Output: An array, which represent an array where each position represents temperatures[ith] indicating how many days we would have
to wait in order to get a warmer temperature.

- Assumptions: Can our temperatures array be empty?, what do we do if we could not find hotter days? (set current index at array to zero), how long is it?

Ok, so we know our current array length will be exactly the same as the given temperatures[]
we need to keep track of our current temperature and simply iterate over the collection.
Once we start at n, we need a way to know what our future elements in the array are and also keep track of them

Could we use 2 pointers?
Would we need to do nested operations? (TLE warning for large arrays)

"""


temperatures = [73,74,75,71,69,72,76,73]
sol = Solution()

res = sol.dailyTemperatures(temperatures)
print("RES: ", res)