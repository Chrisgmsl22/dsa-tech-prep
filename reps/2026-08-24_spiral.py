class Solution:
     def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        result: list[int] = []
        rows, cols = len(matrix), len(matrix[0])
        UP = 0
        RIGHT = cols - 1
        DOWN = rows  - 1
        LEFT = 0 # These are our starting points for iterating, the idea is to shrink them as we go

        while UP <= DOWN and LEFT <= RIGHT: # As long as they don't pass each other, we are within valid bounds
            # Iterate UP
            for i in range(LEFT, RIGHT + 1):
                cell = matrix[UP][i]
                result.append(cell)
            UP += 1
            # Iterate RIGHT
            for i in range(UP, DOWN + 1):
                cell = matrix[i][RIGHT]
                result.append(cell)
            RIGHT -= 1
            
            # Make sure its a squared matrix, otherwise we will reuse cells
            if not (UP <= DOWN and LEFT <= RIGHT): break

            # Iterare DOWN
            for i in range(RIGHT, LEFT - 1, -1):
                cell = matrix[DOWN][i]
                result.append(cell)
            DOWN -= 1
            
            # Iterate LEFT
            for i in range(DOWN, UP - 1, - 1):
                cell = matrix[i][LEFT]
            LEFT += 1
        return result



sol = Solution()

matrix = [[1,2,3],[4,5,6],[7,8,9]]
res = sol.spiralOrder(matrix)
print(res)

"""
    NOTES:
    Ive been trying this exercise for quite a few times already, I think this should be faster, since I know:
    - We need to define boundaries, 4 sides
    - Iteration happens once per side N times, this is a condition we need to find.
    - Since a matrix isnt squared necessarily, we need to define a guard to make sure its within bounds
    - store results in a collector.
    - run code
    - return arr
"""