from collections import defaultdict

class Solution:
    def traverseGraphBFS(self, grid: list[list[int]]) -> None:
        graphMap: dict[int, list[int]] = defaultdict[int, list[int]](list)

        for v1, v2 in grid:
            graphMap[v1].append(v2)
            graphMap[v2].append(v1)
        
        visited = set()
        queue = []

        # Since this is BFS, our queue needs to contain something
        queue.append(grid[0][0])
        visited.add(grid[0][0])

        while queue:
            currVertex = queue.pop(0)
            print(currVertex)

            for neighbor in graphMap[currVertex]:
                # For each one of these, add to queue the ones we have not visited yet
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)



sol = Solution()

grid = [[0, 1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 5]]

sol.traverseGraphBFS(grid)