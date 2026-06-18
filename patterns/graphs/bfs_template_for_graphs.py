""""
    Lets define the barebone structure for BFS on a graph

"""
from collections import deque


class Graph:
    def _buildGraph(self, adjacencyList: list[list[int]]) -> dict[int, list[int]]:
        graph: dict[int, list[int]] = {}

        for vertex1, vertex2 in adjacencyList:
            if vertex1 not in graph:
                graph[vertex1] = []
            if vertex2 not in graph:
                graph[vertex2] = []
            
            graph[vertex1].append(vertex2)
            graph[vertex2].append(vertex1)
        return graph

    def bfs(self, edgeList: list[list[int]]) -> None:
        graph = self._buildGraph(edgeList)
        queue = deque([])
        visited = set()

        # Initialize queue so our code works
        queue.append(edgeList[0][0])
        visited.add(edgeList[0][0])

        while queue:
            currNode = queue.popleft()
            # Process our node
            print(currNode)

            for neighbor in graph[currNode]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)


g = Graph()

edgeList = [[0, 1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 5]]

result = g.bfs(edgeList)