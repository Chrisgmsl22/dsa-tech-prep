""""
You are given an m x n binary matrix grid. An island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water.

The area of an island is the number of cells with a value 1 in the island.

Return the maximum area of an island in grid. If there is no island, return 0.

 

Example 1:


Input: grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
Output: 6
Explanation: The answer is not 11, because the island must be connected 4-directionally.
Example 2:

Input: grid = [[0,0,0,0,0,0,0,0]]
Output: 0
 

"""
from collections import deque


class Solution:
    def maxAreaOfIsland(self, grid: list[list[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        visited = set()
        result = 0

        def bfs(startTuple: tuple[int, int]) -> int:
            queue = deque([])
            queue.append(startTuple)
            visited.add(startTuple)
            currArea = 1 # If we even reach this code, it means we started with a valid 1 in our island

            while queue:
                cI, cJ = queue.popleft()

                for dI, dJ in directions:
                    ctI = dI + cI
                    ctJ = dJ + cJ

                    isNeighborWithinBounds = ctI in range(rows) and ctJ in range(cols)
                    if isNeighborWithinBounds:
                        currT = (ctI, ctJ)
                        if currT not in visited and grid[ctI][ctJ] == 1: # Then perform BFS and keep track
                            currArea += 1
                            visited.add(currT)
                            queue.append(currT)
            return currArea
        
        # Our BFS function is completed, now its time to actually use it
        for i in range(rows):
            for j in range(cols):
                currT = (i, j)
                if currT not in visited and grid[i][j] == 1:
                    # We found a valid start point, start doing BFS
                    currArea = bfs(currT)
                    result = max(result, currArea)

        return result      

    def maxAreaOfIslandDFS(self, grid: list[list[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        visited = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        result = 0

        def dfs(startTuple: tuple[int, int]) -> int:
            visited.add(startTuple)
            area = 1
            sI, sJ = startTuple
            for dI, dJ in directions:
                nI = dI + sI
                nJ = dJ + sJ

                isWithinBounds = nI in range(rows) and nJ in range(cols)
                if isWithinBounds:
                    currTuple = (nI, nJ)
                    if currTuple not in visited and grid[nI][nJ] == 1: # THen its valid, record and do DFS
                        # visited.add(currTuple)
                        area += dfs(currTuple) # Go deeper and increase counter
            
            return area
                   
        for i in range(rows):
            for j in range(cols):
                currT = (i, j)
                if currT not in visited and grid[i][j] == 1:
                    areaOfCurrentIsland = dfs(currT)
                    print("result from DFS: ", areaOfCurrentIsland)
                    result = max(result, areaOfCurrentIsland)
        
        return result




sol = Solution()
grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]

res = sol.maxAreaOfIslandDFS(grid)
print("Final res: ", res)
