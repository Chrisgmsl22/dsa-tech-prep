"""
    Objective: Build a graph from a given list,
    We are given a bi-directional graph into the shape of a list.
    We need to turn it into an adjacency list.

    Let's rememembter that in a bidirectional graph every element is connected to its next element and viceversa
    [1, 0], means vertex 1 is connected to vertex 0, and also vertex 0 is connected to vertex 1. Keep this in mind

"""

# Keep in mind every edge creates 2 entries.
class Solution:
    def convertListIntoAdjacencyList(self, graph: list[list[int]]) -> dict[int, list[int]]:
        res: dict[int, list[int]] = {}
        

        for edge in graph:
            node1, node2 = edge
            print(node1, node2)
            if node1 not in res:
                res[node1] = []
            if node2 not in res:
                res[node2] = []
            print("Current graph: ", res)

            res[node1].append(node2)
            res[node2].append(node1)

        
        return res




sol = Solution()

graph = [[0, 1], [1, 2], [0, 2]]
"""
    Outcome should be like this:
    graph = {
        0: [1, 2],
        1: [0, 2],
        2: [1, 0]
    }


"""

res = sol.convertListIntoAdjacencyList(graph)

print("Result: ", res)