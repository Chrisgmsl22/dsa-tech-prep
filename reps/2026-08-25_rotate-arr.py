class Solution:
    def rotate(self, nums: list[int], k: int) -> None:
        def reverseArr(l: int, r: int) -> None:
            while l <= r:
                nums[l], nums[r] = nums[r], nums[l]
                # Increase pointers
                l += 1
                r -= 1
        
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        tRotations = k % n # 7 / 3 = 2.3 ? => 3
        
        # Revert one time
        reverseArr(0, n - 1) # [7, 6, 5, 4, 3, 2, 1]
        #print(nums)
        # Revert first slice
        l, r = 0, tRotations - 1
        reverseArr(l, r)
        #print(nums)
        # Reverte remaining slice
        l, r = tRotations, n - 1
        reverseArr(l, r)
        #print(nums)
"""
    NOTES:
    - Input: An array of numbers, non sorted and a target k
    - Output: An array of numbers which represent the result of "rotating" the array K times.
    When we say rotate we actually mean the process of moving the array to the right, like in a 2D videogame,
    where once you get to the end, you simply start over from the left.
    So numbers from the right go into the right side.

    Now, the trick here is to be able to tell how this rotation actually happens.
    Moving the entire array is too expensive, we could get an array with 1m elements just to be rotated 5 times.

    So, we need to find the pattern to beat here.
    What is the pattern?
    When we move an array over, elements from the right side end up on the left side, so this is almost as reverting the array.
    
    The difference here is that we need to revert the array, but at the same time slice the array into 2 parts.
    first K rotations

    And last elements after that rotation
    [1, 2, 3, 4, 5, 6, 7] can be turned around
    [7, 6, 5, 4, 3, 2, 1]
    We get top K elements
    [7, 6, 5] 3 because K = 3
    Remaining
    [4, 3, 2, 1]

    We have our slices, we can revert each one individually
    [5, 6, 7] + [1, 2, 3, 4]
    Together they form: [5, 6, 7, 1, 2, 3, 4].

    An important pattern to take into consideration here is that a rotation is cyclic, meaning we will end up with the same answers after K certain rotations.
    [1, 2, 3]
    [3, 1, 2]
    [2, 3, 1]
    [1, 2, 3] Answers simply repeats. This is another pattern we can learn from. And this has a formula
    NORMALIZE THE STEP with % length before anything else.
    len(arr) % k = total amount of rotations?
"""