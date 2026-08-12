class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        result: list[int] = []
        reversedResult: list[int] = []
        # [-4, -1, 0, 3, 10]
        #          l
        #.         r
        # [100, 16, 9,  1, 0]
        # We simply reverse it
        n = len(nums)
        L, R = 0, n - 1
        while L <= R:
            # Compare
            leftNum = nums[L]
            rightNum = nums[R]

            if abs(leftNum) > (rightNum):
                # Means left is the biggest, we use it and move up the pointer
                result.append(leftNum ** 2)
                L += 1
            else:
                # Means right is the biggest, we use it and move down the pointer
                squareVal = rightNum ** 2
                if rightNum == 0:
                    squareVal = 0
                result.append(squareVal)
                R -= 1
        # By this point we will have our answer, we need to reverse it
        #print(result)
        for i in range(n - 1, -1, -1):
            #print(i)
            reversedResult.append(result[i])

        return reversedResult

""""
    NOTES:
    - Input: an array of numbers, which contain their elements SORTED in non-decreasing order
    - Output: an array of numbers, which represents the result of squaring their elements but also keeping the same non-decreasing order.

    Trivial approach would be to square them, then kick off a sort() again, but that would take log(n), so a large data set would take quite a few time.

    our goal would then be to respect the order without a sorting function, how can we do this?

    What we know how to do:
    - Squaring, we just multiply it by itself
    - We know that a square operation returns us a positive value, so we could use an ABS() function to compare
    What I still need to figure out is how are we going to keep track of the order?
    Do we create an empty array? with a fixed size?
    Do we use a stack, no, we dont need to iterate multiple times


    Okay, yes, 2 pointers
    We set one pointer at each side of our array
    We add whichever is our biggest ABS num and append the biggest number (already squared)

    We get our result, we reverse it

"""
