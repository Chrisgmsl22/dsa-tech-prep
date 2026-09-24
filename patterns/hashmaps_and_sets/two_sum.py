class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        numMap: dict[int, int] = {} # Should contain NUMBER as the key, and the value the index
        n = len(nums)

        # [3, 2, 4] t ==> 6


        for i in range(n):
            currNum = nums[i]
            numMap[currNum] = i
        
        for i in range(n):
            currNum = nums[i]
            candidate = target - currNum # 9 - 2 == 7.
            if candidate in numMap and numMap[candidate] != i:
                return [i, numMap[candidate]]

        return [] # Just to comply with linter
"""
    NOTES:
    - Input: an array of numbers, and an integer K
    - Output, an array of numbers, which represent the indices of 2 numbers that summed up equal target

    We can assume there will always be exactly one solution, so there's always going to be answer.
    We can hace repeated values

    We need to be aware of the current indices we have, as well as the values
    We need to traverse our array
    We need to form a collection so we can do constant lookups.

    We already know: Our target, and at least one number (the current number we're on).
    Idea is to keep finding solutions, and as soon as we find our solution, we return the answer, no need to keep traversing.

    Can we split the traversals into 2?

"""