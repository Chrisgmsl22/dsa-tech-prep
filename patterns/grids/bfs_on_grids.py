class Solution:
    def performBfs(self, grid: list[list[int]]) -> list[int]:
        rows, cols = len(grid), len(grid[0])
        queue = [] # We store coordinates, not the direct value
        result = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        visited = set()

        # Mark the start of our queue
        queue.append((0, 0))
        result.append(grid[0][0])
        visited.add((0,0))

        while queue:
            currElement = queue.pop(0)
            i, j = currElement

            for dI, dJ in directions: # This is our iterative approach for the queue
                nI = dI + i
                nJ = dJ + j

                isWithinBounds = nI in range(rows) and nJ in range(cols)
                if isWithinBounds:
                    currNeighbor = (nI, nJ)
                    if currNeighbor not in visited:
                        result.append(grid[nI][nJ])
                        queue.append(currNeighbor)
                        visited.add(currNeighbor)
        
        return result
            



sol = Solution()

grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

res = sol.performBfs(grid)

print("Result: ", res)