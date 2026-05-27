class Solution:
    # In python, adding _ to a method makes it private
    def _convertGridIntoAdjacencyList(self, grid: list[list[int]]) -> dict[int, list[int]]:
        res: dict[int, list[int]] = {}

        for vertex in grid:
            n1, n2 = vertex

            if n1 not in res:
                res[n1] = []
            if n2 not in res:
                res[n2] = []
            
            res[n1].append(n2)
            res[n2].append(n1)
        
        return res

    def traverseGraph(self, grid: list[list[int]]) -> None:
        graph = self._convertGridIntoAdjacencyList(grid)
        print("Current graph: ", graph)
        visited = set()

        def dfs(v: int):
            print(v)
            visited.add(v)
            for neighbor in graph[v]:
                if neighbor not in visited:
                    dfs(neighbor)
        dfs(grid[0][0])
        

sol = Solution()

grid = [[0, 1], [1, 2], [0, 2]]
grid2 = [[0, 1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 5]]

sol.traverseGraph(grid2)