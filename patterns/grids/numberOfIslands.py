"""
    Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.

"""

class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        visited = set()
        result = 0
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def recurse(i: int, j: int):
            # base case condition?
            visited.add((i, j)) # We add a tuple
            
            for dI, dJ in neighbors:
                neighborI = dI + i
                neighborJ = dJ + j


                isNeighborValid = neighborI in range(rows) and neighborJ in range(cols)

                if isNeighborValid:

                    possibleTuple = (neighborI, neighborJ)
                    if possibleTuple not in visited: # new combination
                        if grid[neighborI][neighborJ] == "1":
                            print(grid[neighborI][neighborJ])
                            recurse(neighborI, neighborJ) # Will only recurse on existing 1's
                        
        
        for i in range(rows):
            for j in range(cols):
                t = (i, j)
                if t not in visited and grid[i][j] == "1":
                    result += 1
                    recurse(i, j) # Start DFS once a new island is found


        
        return result

    def numIslandsBfs(self, grid: list[list[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        visited: set[tuple[int, int]] = set()
        result = 0

        
        def bfs(i: int, j: int):
            queue = [] # Can also import from collections.dequeue
            queue.append((i, j))
            visited.add((i, j))

            while queue:
                r, c = queue.pop(0)
                
                # Explore closest neighbors for current cell
                for dI, dJ in neighbors:
                    nI = dI + r
                    nJ = dJ + c

                    isNeighborValid = nI in range(rows) and nJ in range(cols)
                    if isNeighborValid:
                        currT = (nI, nJ)
                        if currT not in visited and grid[nI][nJ] == "1":
                            queue.append(currT)
                            visited.add(currT)

        
        for i in range(rows):
            for j in range(cols):
                currT = (i, j)
                if currT not in visited and grid[i][j] == "1":
                    # Then its a new island
                    bfs(i, j)
                    result += 1

        return result




sol = Solution()

grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"], # Island happens at the very first element at the left at this level
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]

res = sol.numIslandsBfs(grid)

print("Final result: ", res) # Should be 1


"""
    For this problem we need to form crosses. Because an island is a number 1 that has a 1 UP, DOWN, LEFT and RIGHT.
    The catch is that on the edges of the grid are all surrounded by water. Correction, we don't need all 4 sides. We only need UP-DOWN or LEFT-RIGHT, an island may have both, but it is not necessary

    So we need to go over the whole grid and check if the current element is an island. So we check if UP-DOWN and/OR LEFT-RIGHT == "0", then it is an island, we increase a counter by 1
    BUT also, if the current number IS on the edge, then that edge can be counted as 1. How do we check this?

    We go over the whole grid, collect islands and lastly we return the final number.

"""