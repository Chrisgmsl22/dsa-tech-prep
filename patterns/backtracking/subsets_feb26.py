class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        allSubsets = []
        tempSubset = []
        def recurse(i: int):
            if i == len(nums):
                # We've reached the end of our run
                allSubsets.append(tempSubset[:]) # Shallow copy
                return
            
            recurse(i + 1) # First branch, don't append

            tempSubset.append(nums[i])
            recurse(i + 1)

            # Bracktrack
            tempSubset.pop()
        
        recurse(0)
        return allSubsets


""" 
    NOTES.
    - Input: An array of UNIQUE elements
    - Output: An array of arrays
    The goal is to generate all possible subsets with the number's we're given
    What is a subset? ==> A selection of elements from an original array, since a set
    already needs to contain unique values, this means our subset also need to contain unique
    values

    Our goal is to generate all subsets possibles.
    For this we can build a mental tree, binary tree to be specific. Because our left branch will indicate that we decide not to include it, or to actually include it.

    For this we will need to go over the array of nums (could this be a simple for i in range_
    ?), and for each number we will decide wether or not we add the element to out mini array

    An additional important note here is that the way we move through trees is using recursion, where each recursion call will correspond to each branch (binary tree -> 2 branches -> 2 recursive calls)

    So we iterate over this, we get the number, and built our array.
    How do we know when to stop? TBD
"""