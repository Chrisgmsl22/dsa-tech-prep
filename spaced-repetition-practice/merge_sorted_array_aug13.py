class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        p1, p2, p3 = m - 1, n - 1, m + n - 1


        # Define our condition to constantly iterate
        # [4, 5, 6, 4, 5, 6] m = 3
    #    p1
        #.       p3
        # [1, 2, 3] n = 3
    #            p2

        # We should be going backwards
        while p3 >= 0 and p2 >= 0:
            if p1 < 0:
                print("Ran out of p1s")
                nums1[p3] = nums2[p2]
                p2 -= 1
            elif nums1[p1] > nums2[p2]:
                # Insert biggest into current p3
                print("nums1 is bigger: ", nums1[p3])
                nums1[p3] = nums1[p1]
                #nums1[p1] = 0 # Confirm this approach is valid
                p1 -= 1
            else:
                print("nums2 is bigger: ", nums1[p3])
                nums1[p3] = nums2[p2]
                p2 -= 1
            print(nums1)
            p3 -= 1
"""
    NOTES:
    - Input: 2 arrays that are already sorted, may contain negative
    And 2 numbers, which represent the number of elements of the 2 previous arrays
    - Output: an array, which represents the union of both arrays that are already sorted.
    Answer should basically return the 2 arrays merged while keeping the same order.

    Something important to consider is that we can use the arrays being already sorted to our advantage.
    We have 2 challenges.
    This is a 2 pointers problem, we're going to point 1 pointer to one array, one to another.
    We constantly compare which one is bigger, if thats the case, we add that one and so on.
    We do not need a new array, we will use nums1 as the point of reference and return nothing.

    second challenge is when we are out of bounds, meaning we simply ran out of  elements in the array.
    In this case we already know the result is already merged, so we can simply append the rest

    Seems like we already have a fixed size for our array, we could simply add in-place

    Need to shift everything to the right if there are no zeros

"""
