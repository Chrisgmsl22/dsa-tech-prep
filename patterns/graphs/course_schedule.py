"""
There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
Return true if you can finish all courses. Otherwise, return false.



Example 1:

Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: There are a total of 2 courses to take.
To take course 1 you should have finished course 0. So it is possible.
Example 2:

Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: There are a total of 2 courses to take.
To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.

"""


class Solution:
    def _buildAdyacencyList(self, adList: list[list[int]]) -> dict[int, list[int]]:
        graph: dict[int, list[int]] = {}

        for group in adList:
            v1, v2 = group

            if v1 not in graph:
                graph[v1] = []
            graph[v1].append(v2)
        return graph

    # {0: [1], 1: [0]}
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        adjList = self._buildAdyacencyList(prerequisites)
        visited = set()
        result = [True]

        inProgress = set()

        def dfs(node: int):  # Node will represent the key from our adjList
            # visited = (0, 1)
            print(node)
            visited.add(node)
            inProgress.add(node)

            if node in adjList:
                for neighbor in adjList[node]:
                    if neighbor not in visited and neighbor in adjList:
                        # If not visited, then we can process
                        dfs(neighbor)
                    else:
                        if neighbor in inProgress:
                            result[0] = False

            inProgress.remove(node)

        for course in range(numCourses):
            dfs(course)
        return result[0]


numCourses = 20
preReq = [[1, 0], [0, 1]]
data = [[1, 0]]
testData = [[1, 0], [3, 2]]
testData2 = [[0, 10], [3, 18], [5, 5], [6, 11], [11, 14], [13, 1], [15, 1], [17, 4]]

res = Solution()

print(res.canFinish(numCourses, testData2))
