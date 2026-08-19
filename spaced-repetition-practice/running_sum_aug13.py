class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result: list[int] = [0] * n
        accumulator = 0

        for i in range(n):
            accumulator += nums[i]
            result[i] = accumulator

        return result


"""
    NOTES:
    - Input: array of numbers, not sorted, numbers can be negative
    - Output: An array of the same size as the input, where each position holds an accumulated sum by that point

    Need to accumulate our sum as we go.
    running sum contains the current number + the previous accumulated sum by that point

    Normal iteration
    Once we reach the end, we will have found our answer
    Need to use extra space to define the resulting array

"""
