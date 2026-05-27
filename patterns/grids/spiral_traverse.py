class Solution:
    def traverseInSpiral(self, grid: list[list[int]]) -> list[int]:

        rows = len(grid)
        cols = len(grid[0])

        TOP = 0 # row
        LEFT = 0 # column
        
        BOTTOM = rows - 1 # row
        RIGHT = cols - 1 # column
        
        totalElementsInGrid = rows * cols
        result = [] # This will contain the numbers in the correct traverse order

        while len(result) != totalElementsInGrid: # As long as we have elements, then keep iterating
            # Top (goes right), row is fixed, column is dynamic
            if TOP <= BOTTOM:
                for i in range(LEFT, RIGHT + 1):
                    result.append(grid[TOP][i])
                    print(result)
                TOP += 1

            # Right (goes down)
            if LEFT <= RIGHT:
                for i in range(TOP, BOTTOM + 1):
                    result.append(grid[i][RIGHT])
                    print(result)
                RIGHT -= 1

            # Bottom (goes left)
            if TOP <= BOTTOM:
                for i in range(RIGHT, LEFT - 1, -1):
                    result.append(grid[BOTTOM][i])
                    print(result)
                BOTTOM -= 1
        

            # Left (goes up)
            if LEFT <= RIGHT:
                for i in range(BOTTOM, TOP - 1, -1):
                    result.append(grid[i][LEFT])
                    print(result)
                LEFT += 1

            # After we do this, we shrink the box and let the loop contine ierating
            
        return result



sol = Solution()

grid = [
    [1, 2, 3, 3],
    [4, 5, 6, 6],
    [7, 8, 9, 9]
] # 1, 2, 3, 3, 6, 9, 9, 8, 7, 4, 5, 6
grid2 = [[1, 2, 3]] # [1, 2, 3], single row

grid3 = [
    [1], 
    [2],
    [3],
    [4]
] # [1, 2, 3, 4], single column

res = sol.traverseInSpiral(grid3)

""""
     [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]

    top: topmost row
    right: rightmost col
    bottom: bottommost row 
    left: leftmost col

    
    left: starts at

"""