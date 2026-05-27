""" ''
    you write a function that:

  1. Takes a 2D grid of integers
  2. Traverses every element
  3. Returns the sum of all elements



"""
class Solution:
    def grid_sum(self, grid: list[list[int]]) -> int:
        # We need to traverse the whole grid, and collect each element along the way
        res = 0

        # Row level
        for i in range(len(grid)):

            # Cell level
            for j in range(len(grid[i])):
                print(f"Level: {grid[i]}, cell: {grid[i][j]}")
                res += grid[i][j]
        return res
    
    def grid_sum_2(self, grid: list[list[int]]) -> int:
        res = 0

        for row in grid:
            for column in row:
                res += column
        
        return res
    

sol = Solution()
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

res = sol.grid_sum_2(grid)
print(res)
