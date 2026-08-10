"""
Given an m x n matrix, return all elements of the matrix in spiral order.

Example 1:
Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]
Example 2:

Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
Output: [1,2,3,4,8,12,11,10,9,5,6,7]


"""
class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        result: list[int] = []
        rows, cols = len(matrix), len(matrix[0])
        up = 0
        right = cols - 1
        down = rows - 1
        left = 0

        while up <= down and left <= right:
            # Iterate UP
            print("iterating")
            u = up
            while u == up:
                for i in range(left, right + 1):
                    result.append(matrix[u][i])
                up += 1
            # Iterate RIGHT

            r = right
            while r == right:
                for i in range(up, down + 1):
                    result.append(matrix[i][r])
                right -= 1
            # Iterate DOWN
            d = down
            while d == down:
                for i in range(right, left - 1, -1):
                    result.append(matrix[d][i])
                down -= 1

            # Iterate LEFT
            l = left
            while l == left:
                for i in range(down, up - 1, -1):
                    result.append(matrix[i][l])
                left += 1
            print('result: ', result)
        return result

sol = Solution()
"""
    [
        [1, 2, 3]
        [4, 5, 6]
        [7, 8, 9]
    ]
"""
matrix = [[1,2,3],[4,5,6],[7,8,9]]
res = sol.spiralOrder(matrix)

#print("OUTPUT: ", res)

"""
    NOTES:
        - Input: a 2D array
        - Output: a 1D array, which represents a spiral traversal order in which we simply add our values to the array

        Brainstorm:
            We need to be able to traverse through a 2D array, for this we can start from the basics, so 1D, horizontally, but how could we traverse vertically?

            We are going to need pointers, and possibly an inner iteration.
            We are also going to need a way to restrict ourselves from going over the same iteration, we will need some sort of mental barrier.

            Also, we need to account for a m x n matrix, so the size is not fixed, it is dynamic, we also need to account for this
"""
