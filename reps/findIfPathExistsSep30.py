class Solution:
    def validPath(self, n: int, edges: list[list[int]], source: int, destination: int) -> bool:
        if not edges: return True

        graphMap: dict[int, list[int]] = {}
        visited = set()
        queue = [] # Could use dequeue

        # Build graphMap
        for edge in edges:
            ui, vi = edge
            
            if ui not in graphMap:
                graphMap[ui] = []
            if vi not in graphMap:
                graphMap[vi] = []
            graphMap[ui].append(vi)
            graphMap[vi].append(ui)
        # {0: [1], 1: [2], 2: [0]}

        #print(graphMap)

        queue.append(source) # Starting point
        visited.add(source)

        while queue:
            currVertex = queue.pop(0) # popleft()
            #print(currVertex)
            for neighbor in graphMap[currVertex]:
                #print(neighbor)
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return source in visited and destination in visited
"""
    NOTES:
    - Input: an array of edges, which represent a graph, a source node and a destination node
    - Output: boolean, which represents the result of checking if we can find a path from source to destination. (if they're connected)

    This is a graph problem, before traversing through the graph, we need to define a proper structure to hold them.
    Given that a graph connects several nodes together, we need to keep track of the nodes

    We can use a hashMap to store the current locations

    Once this is done we need to traverse through the actual graph, for each vertex, we traverse it, we can use
    either DFS (recursion) or BFS (queues), goal is to see if the same vertex is found, maybe we could use a hashSet or something
    like that

    If we find them, then it means it was found

"""