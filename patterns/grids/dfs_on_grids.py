class Solution:
    def performDfsOnGrid(self, grid: list[list[int]]) -> None:
        rows = len(grid)
        cols = len(grid[0])
        
        visitedCells = set() # This will be a set of tuples
        neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)] # Up, down, left, right neighbors (i, j)
        def recurse(i, j):
            visitedCells.add(i,j) # We mark ourselves before anything else happens            

            print(grid[i][j])
            for cI, cJ in neighbors:
                # Calculate neighbor
                neighbor_i = cI + i
                neighbor_j = cJ + j
                # Check bounds
                is_neighbor_i_valid = neighbor_i >= 0 and neighbor_i < len(grid)
                is_neighbor_j_valid = neighbor_j >= 0 and neighbor_j < len(grid[0])

                if is_neighbor_i_valid and is_neighbor_j_valid:
                    # Check visited
                    neighbor_tuple = (neighbor_i, neighbor_j)
                    if neighbor_tuple not in visitedCells:
                        # Now we are safe, we print, and we save the value
                        #print(grid[neighbor_i][neighbor_j])
                        visitedCells.add(neighbor_tuple)

                        # recurse
                        recurse(neighbor_i, neighbor_j)
                        #visitedCells.remove(neighbor_tuple) # Backtrack?

                    # Else, do nothing
        recurse(0, 0)

    def performDfsOnGrid2(self, grid: list[list[int]]) -> None:
        visited = set()
        neighbors = [(-1 ,0), (1, 0), (0, -1), (0, 1)] # UP, DOWN, LEFT, RIGHT references for getting each neighbor

        def recurse(i: int, j: int):
            # Stop condition will be taken care when out loop ends, no need to add an if check here
            visited.add((i, j))
            print(grid[i][j])
            for n_i, n_j in neighbors:
                neighbor_i = n_i + i
                neighbor_j = n_j + j

                # Is coordinates within the grid range
                is_neighbor_i_valid = neighbor_i >= 0 and neighbor_i < len(grid) # i is for row axis
                is_neighbor_j_valid = neighbor_j >= 0 and neighbor_j < len(grid[0])

                if is_neighbor_i_valid and is_neighbor_j_valid:
                    possible_tuple = (neighbor_i, neighbor_j)
                    if possible_tuple not in visited:
                        recurse(neighbor_i, neighbor_j)

        recurse(0, 0)



#sol = Solution()
#grid = [
#    [1, 2, 3],
#    [4, 5, 6],
#    [7, 8, 9]
#]

#print(sol.performDfsOnGrid2(grid))

"""
    So now you have all the pieces for grid DFS:

  1. Directions array — to find neighbors
  2. Bounds checking — to stay inside the grid
  3. Visited set — to avoid infinite loops
  4. Recursion — to go deep before going wide

"""