class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        res = 0 # Counter
        visited = set()
        queue = [] # dequeue from the collections library
        directions: list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)] # L, R, U, D

        # Build adjacency list (actual graph to know where each node is connected to)
        def bfs(t: tuple[int, int]):
            queue.append(t)
            visited.add(t)

            while queue:
                i, j = queue.pop(0) # dequeue.popleft()

                for direction in directions:
                    dI, dJ = direction
                    newI, newJ = dI + i, dJ + j

                    isNeighborValid = newI in range(rows) and newJ in range(cols)
                    if isNeighborValid: # If its within bounds
                        neighborT = (newI, newJ)
                        if neighborT not in visited and grid[newI][newJ] == "1": # and its actually land
                            visited.add(neighborT) # Keep doing BFS
                            queue.append(neighborT)

        
        # Goal is to traverse via BFS as soon as we find a 1
        for i in range(rows):
            for j in range(cols):
                currT = (i, j)
                if currT not in visited and grid[i][j] == "1":
                    # we have a valid island starting point
                    res += 1
                    bfs(currT)
        
        return res



"""
    NOTES:
    - Input: a m X n 2D binary grid (a 2D array with 1s and 0s wrapped in strings)
    - Output: Number, which represents the total number of islands represented in the grid.

    Goal is to find all possible islands in the given grid. This means we may have a lot more islands in one single place. So, how do we know an island is an island?, we do this by checking all connected 1s that are surrounded by water (zeros). Once we find a land, we need to search and see how far this insland goes.

    We start checking all contents of this island, and once we are out of 1s, we have finished our current run, we can increase a counter or something like that.

    We move on in the grid, we will need to have a hash set to keep track of the "visited" coordinates, as soon as we find a new one, we start the process all over again

    By the time we reach the end, we will have found all of our islands, and we return the answer.

    We need to make a traversal, and also use a BFS so we can expand horiontally rather than a DFS. So for this we need to use a queue, and we need to build an adjacency list

"""