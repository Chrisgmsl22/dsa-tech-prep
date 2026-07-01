"""
You are given an integer array cost where cost[i] is the cost of ith step on a staircase. Once you pay the cost, you can either climb one or two steps.

You can either start from the step with index 0, or the step with index 1.

Return the minimum cost to reach the top of the floor.



Example 1:

Input: cost = [10,15,20]
Output: 15
Explanation: You will start at index 1.
- Pay 15 and climb two steps to reach the top.
The total cost is 15.
Example 2:

Input: cost = [1,100,1,1,1,100,1,1,100,1]
Output: 6
Explanation: You will start at index 0.
- Pay 1 and climb two steps to reach index 2.
- Pay 1 and climb two steps to reach index 4.
- Pay 1 and climb two steps to reach index 6.
- Pay 1 and climb one step to reach index 7.
- Pay 1 and climb two steps to reach index 9.
- Pay 1 and climb one step to reach the top.
The total cost is 6.

"""


class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        memo: dict[int, int] = {}

        def recurse(i: int) -> int:
            # print(i, cost[i])
            if i in memo:
                return memo[i]
            if i == 0 or i == 1:
                return cost[i]  # If i == n we would have reached the top
            option1 = recurse(i - 1)
            option2 = recurse(i - 2)
            compute = cost[i] + min(option1, option2)

            memo[i] = compute
            return memo[i]

        return min(
            recurse(len(cost) - 1), recurse(len(cost) - 2)
        )  # We start from the top, we go back from there


sol = Solution()
cost = [10, 15, 20]

res = sol.minCostClimbingStairs(cost)
print("Result: ", res)
