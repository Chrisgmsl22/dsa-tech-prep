class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        n = len(numbers)
        L, R = 0, n - 1
        # [2, 7, 11, 15], t = 9
        #  L
        #            R
        # We compute, our current sum, if its too big, we shrink R, if its too small, we grow L, if we find a match, store and BREAK
        while L < R:
            leftVal = numbers[L]
            rightVal = numbers[R]
            currentSum = leftVal + rightVal

            if currentSum == target:
                # Store them and break
                return [L + 1, R + 1]
            elif currentSum > target:
                # Too big, shrink R
                R -= 1
            else:
                # Too small, grow L
                L += 1




""""
    NOTES:
    - Input: An array of SORTED numbers, our array is 1-indexed, meaning its first value is considered index 1, not 0, and a target T, which represents the target we can find
    - Ouput: A tuple, or an array with only 2 numbers, which represent the 1-indixes that add up to a target

    There is exactly one solution, so there will always be an answer.

    We need to use as information what they tell us, the given array is already sorted, so this means we can do a 2 pointer approach where we compare smallest VS biggest and adjust our pointers from there.

    Once we have found a match, there is no need to continue iterating, we can BREAK.
    Since there is always one answer, we can do a while True, so we iterate all the time, or maybe use L and R as our condition.

    Once we find our indices we append their number with a + 1, because we are asked to return the 1-index version for those arrays.

"""
