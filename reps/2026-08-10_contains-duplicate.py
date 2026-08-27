class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:

        """
        for num in nums:
            if num not in seen:
                seen.add(num)
            else:
                return True
        return False
        """
        numsSize = len(nums)
        numsSet = set(nums)
        numsSetSize = len(numsSet)

        return numsSize != numsSetSize

"""
    NOTES:
    - Input: An array of numbers, which may contain repeated elements
    - Output: boolean, which represents the evaluation of checking if the element is repeated in the array.

    Goal is to find out if our array contains a duplicate
    There are quite a few different ways to do this

    We can check its length, then turn it into a set and simply return the comparison of lengths
    Easiest approach is a single iteration + an additional data structure for comparing if we've seen the value
    The advantage of this approach is that as soon as we know there is a problem, we stop

    Turning the other whole array into a set might take more time in computation

"""
