"""
    8. Generate All Subsets (Medium)
    Problem: Generate all subsets of a set
    Example: subsets([1,2]) = [[], [1], [2], [1,2]]
    Think: For each element, you make a choice:

    Include it
    Exclude it
"""


def generateSubsets(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    finalAns = []
    currSubset = []

    def backtrackHelper(idx: int):
        # What is the base case here?
        if idx == n:
            finalAns.append(currSubset[:])
            return

        backtrackHelper(idx + 1)

        currSubset.append(nums[idx])
        backtrackHelper(idx + 1)

        # Backtrack
        currSubset.pop()

    backtrackHelper(0)
    return finalAns


testInput = [1, 2, 3]
print(generateSubsets(testInput))
