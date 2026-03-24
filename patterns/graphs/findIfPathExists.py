"""
There is a bi-directional graph with n vertices, where each vertex is labeled from 0 to n - 1 (inclusive). The edges in the graph are represented as a 2D integer array edges, where each edges[i] = [ui, vi] denotes a bi-directional edge between vertex ui and vertex vi. Every vertex pair is connected by at most one edge, and no vertex has an edge to itself.

You want to determine if there is a valid path that exists from vertex source to vertex destination.

Given edges and the integers n, source, and destination, return true if there is a valid path from source to destination, or false otherwise.

Input: n = 3, edges = [[0,1],[1,2],[2,0]], source = 0, destination = 2
Output: true
Explanation: There are two paths from vertex 0 to vertex 2:
- 0 → 1 → 2
- 0 → 2
Example 2:


Input: n = 6, edges = [[0,1],[0,2],[3,5],[5,4],[4,3]], source = 0, destination = 5
Output: false
Explanation: There is no path from vertex 0 to vertex 5.

"""
class Solution:
    def _buildGraphMap(self, grid: list[list[int]]) -> dict[int, list[int]]:
        graphMap: dict[int, list[int]] = {}

        for vertices in grid:
            v1, v2 = vertices

            if v1 not in graphMap:
                graphMap[v1] = []
            if v2 not in graphMap:
                graphMap[v2] = []
            graphMap[v1].append(v2)
            graphMap[v2].append(v1)

        return graphMap
    def validPath(self, n: int, edges: list[list[int]], source: int, destination: int) -> bool:
        graphMap = self._buildGraphMap(edges)
        visited = set()
        timesValid = 0 # If this is greater than 0, then we know its valid
        print(graphMap)
        def dfs(v: int) -> bool:
            print(v, destination)
            if v == destination:
                return True
            visited.add(v)

            for neighbor in graphMap[v]:
                
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
            return False
        return dfs(source)
    
    def validatePathUsingBFS(self, n: int, edges: list[list[int]], source: int, destination: int) -> bool:
        graph = self._buildGraphMap(edges)
        visited = set()
        queue = []

        queue.append(source)
        visited.add(source)

        while queue:
            currV = queue.pop(0)
            if currV == destination:
                return True
            
            for neighbor in graph[currV]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
        
        return False


# Remember, if my recursive function returns a value, then we need to connect it with the rest of the other recursive calls, so we do return dfs() ...

# If my recursive call does not return us anything, then we do not need to return dfs() we simply call the function

sol = Solution()

n = 3 
edges = [[0,1],[1,2],[2,0]] 
source = 0 
destination = 2

res = sol.validatePathUsingBFS(n, edges, source, destination)

print("Result: ", res)