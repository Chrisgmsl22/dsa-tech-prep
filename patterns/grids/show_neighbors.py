

class Solution:
    def showNeighbors(self, grid: list[list[int]], i: int, j: int) -> list[int]:
        # UP, DOWN, LEFT and RIGHT
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        # We are saying: "Move row by minus one and column by 0"
        for di, dj in directions:
            neighbor_i = i + di
            neighbor_j = j + dj
            # Imporant: Don't forget to check if current coordinates are not out of bounds
            isNeighborIValid = neighbor_i >= 0 and neighbor_i < len(grid)
            isNeighborJValid = neighbor_j >= 0 and neighbor_j < len(grid[0])
            if (isNeighborIValid and isNeighborJValid):
                currNeighbor = grid[neighbor_i][neighbor_j]
                neighbors.append(currNeighbor)


        return neighbors
        # 5, 2, 8, 4, 6
        # Show neighbords, for this, we would consider a neighbor to be 1 step BEFORE of AFTER the center
        # Left and Up are before the center
        # Right and down are after the center





sol = Solution()
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

res = sol.showNeighbors(grid, 0, 0)
print(res)