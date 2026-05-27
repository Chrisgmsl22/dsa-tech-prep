"""


"""
class Graph:
    def _buildAdjacentyList(self, grid: list[list[int]]) -> dict[int, list[int]]:
        graph: dict[int, list[int]] = {}

        for vertice in grid: #[this, this]
            v1, v2 = vertice
            if v1 not in graph:
                graph[v1] = []
            if v2 not in graph: # We do this because it is a bidirectional graph
                graph[v2] = []
        
            graph[v1].append(v2)
            graph[v2].append(v1)
        return graph
    def traverseGraphUsingDFS(self, grid: list[int[int]]) -> None:
        graph = self._buildAdjacentyList(grid)
        visited = set()
        print(graph)

        def recurse(node: int):
            print(node)
            visited.add(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    recurse(neighbor)
        
        recurse(grid[0][0])



g = Graph()

grid = [[0, 1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 5]]

result = g.traverseGraphUsingDFS(grid)