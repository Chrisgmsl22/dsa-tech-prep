class Solution:
    def traverseVertically(self, grid: list[list[int]]) -> None:
        # For a regular traverse, we do row by bow
        # For a vertical traverse, we should do column by column
        totalRows = len(grid)
        for c in range(len(grid[0])):
            
            for r in range(len(grid)):
                print(grid[r][c])
    
        
        # Notice how
        #print(grid[0][0], grid[1][0], grid[2][0])
        #print(grid[0][1], grid[1][1], grid[2][1])
        #print(grid[0][2], grid[1][2], grid[2][2])
            
    def traverseVertically2(self, grid: list[list[int]]) -> None:
        for i in range(len(grid)):
            for j in range(len(grid)):
                print(grid[j][i])


sol = Solution()
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

sol.traverseVertically2(grid)

""""

    When it comes to vertical traversal, it makes sense to focus on each COLUMN first
    and THEN ROW

    If its a normal traversal, then we will go through each ROW first, then COLUMN

    The normal way to traverse a grid is on grid[row][column]
    The order in which we traverse (vertical VS horizontal) will be determined by how we define our loops

    for HORIZONTAL: go through row first loop, column inner loop
    VERTICAL: go through column first, row inner loop

        BOTH WILL BE TRAVERSED BY DOING grid[row][column]

        AGAIN, WHAT MATTERS IS THE ORDER IN WHICH WE DEFINE OUR LOOPS

"""