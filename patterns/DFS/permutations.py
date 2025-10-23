"""
    Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.

 

    Example 1:

    Input: nums = [1,2,3]
    Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
    Example 2:

    Input: nums = [0,1]
    Output: [[0,1],[1,0]]
    Example 3:

    Input: nums = [1]
    Output: [[1]]

    

    Constraints:

        1 <= nums.length <= 6
        -10 <= nums[i] <= 10
        All the integers of nums are unique.

    A permutation is the arrangement of the elements inside an array

"""
def permute(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    finalAns = []
    currentPermutation = []

    def backtrack_helper():
        print(currentPermutation)
        # What is the base case?
        if len(currentPermutation) == n: # Then we've reached a base case, we add it to the list and we return
            finalAns.append(currentPermutation[:])
            return

        # If we are not paying attention to the index, then we don't need it, we simply do a regular for each
        for currNum in nums: # Iterate over all elements on every call, make sure we dont use a number thats already been used
            if currNum not in currentPermutation: # It means we have not used it yet, so we can use it
                currentPermutation.append(currNum)
                backtrack_helper()

                currentPermutation.pop() # Backtrack
        print("End of iteration")


    backtrack_helper()
    return finalAns






nums = [1,2,3]
print(permute(nums))
