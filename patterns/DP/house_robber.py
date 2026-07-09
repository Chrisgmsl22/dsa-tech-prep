"""
You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.



Example 1:

Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.
Example 2:

Input: nums = [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
Total amount you can rob = 2 + 9 + 1 = 12.
"""


# [1, 2, 3, 1]]
# Do we need to start from the beggining?
# Our goal would be to get as much cash as possible
# DP, identify overlapping problems
# 1 + 3 || 2 + 1 = 4 vs 3, 4 wins
# [1], then 1 is my answer
# [1, 2], then 2 is my answer, 2 is the biggest
# [1, 2 ,3] =
class Solution:
    def rob(self, nums: list[int]) -> int:
        memo: dict[int, int] = {}

        # Lets define our base cases first
        def recurse(idx: int) -> int:
            if idx in memo:
                return memo[idx]
            if idx == 0:  # Only one house, then rob it
                return nums[0]
            if idx == 1:  # 2 houses, pick which ever has the biggest val
                return max(nums[0], nums[1])

            robHouse = nums[idx] + recurse(idx - 2)
            skipHouse = recurse(idx - 1)
            winner = max(robHouse, skipHouse)
            memo[idx] = winner
            return memo[idx]

        return recurse(
            len(nums) - 1
        )  # We start from the end, and iterate towards base case


sol = Solution()
houses = [1, 2, 3, 1]

res = sol.rob(houses)
print("Final result: ", res)
