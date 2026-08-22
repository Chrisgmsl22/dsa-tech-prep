class Solution:
    def rotate(self, nums: list[int], k: int) -> None:
        def rotateBetween2Indices(l: int, r: int) -> None:
            while l <= r:
                nums[l], nums[r] = nums[r], nums[l]
                l += 1
                r -= 1
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        k %= n

        # Rotate once
        rotateBetween2Indices(0, n - 1)
        firstK = k - 1
        lastK = firstK + 1

        # Reverse those 2
        l = 0
        r = firstK
        rotateBetween2Indices(l, r)
        #print("nums after 1st reverse loop: ", nums)

        l = lastK
        r = n - 1
        rotateBetween2Indices(l, r)


        # [7, 6, 5, 4, 3, 2, 1]
        #        l
        # [      ] first K
        #           [         ] last len - k
        # [5, 6, 7] [1, 2, 3, 4]


"""
    NOTES:
    - Input: an array of numbers, with values that may contain negatives and a target K, which represents how many times we have to "rotate" the array, which, in my mind sounds like moving the elements to the right, like a 2D videogame where you show up on the left after going too much on the right

    The trick here is to move everythin?, or just the top K elements on the left and right of our array
    Shifting everything would be too much compute, and might even hit TLE.

    Extra space is the only solution, where I define 2 pointers, and make sure to append them in order, first the range of the right pointer, and then the range of the left pointer.

    But the problem is asking for a constant solution
    A useful tip is to reverse the array, but how could this help us?


"""
