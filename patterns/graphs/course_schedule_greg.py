class Solution:
    def _buildAdyacencyList(self, adList: list[list[int]]) -> dict[int, list[int]]:
        graph: dict[int, list[int]] = {}

        for group in adList:
            v1, v2 = group

            if v1 not in graph:
                graph[v1] = []
            graph[v1].append(v2)
        return graph

    def canFinish(self, numCourses: int, prereq: list[list[int]]) -> bool:
        graph = self._buildAdyacencyList(prereq)
        UNVISITED = 0
        VISITING = 1
        VISITED = 0
        states = [UNVISITED] * numCourses

        def dfs(node: int) -> bool:
            currState = states[node]
            if currState == VISITED:
                return True
            if currState == VISITING:
                return False

            states[node] = VISITING

            for neighbor in graph[node]:
                # Traverse
                valid = dfs(neighbor)
                if not valid:
                    return False
            # By this point, we will already have finished visiting our node
            states[node] = VISITED
            return True

        for course in range(numCourses):
            valid = dfs(course)
            if not valid:
                return False
        return True


numCourses = 20
preReq = [[1, 0], [0, 1]]
data = [[1, 0]]
testData = [[1, 0], [3, 2]]
testData2 = [[0, 10], [3, 18], [5, 5], [6, 11], [11, 14], [13, 1], [15, 1], [17, 4]]

res = Solution()

print(res.canFinish(numCourses, testData2))
