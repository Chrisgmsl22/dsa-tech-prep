class Solution:
    def combine(self, n: int, k: int) -> list[list[int]]:
        ans: list[list[int]] = []
        temp = []
        def dfs(start: int):
            print(temp)
            if len(temp) == k:
                ans.append(temp[:])
                return
            for num in range(start, n + 1): # Go over all numbers
                print("temp so far: ", temp)
                temp.append(num)
                dfs(num + 1)

                # Backtrack
                temp.pop()

        dfs(1)
        return ans 

sol = Solution()
n = 4
k = 2

res = sol.combine(n, k)
print("Final result: ", res)

"""
    NOTES:
    - Input: two numbers
    - Output: A list of lists of numbers, which represent the total amount of possible combinations made for the numbers given

    Now, we definitely need recursion here. More specifically: DFS with backtracking,
    We need to define our combinations by picking from the numbers in the range.
    Our constraints: Same number cannot be used twice, and combination array size should be of size K all the time.

    Once we have this, we append the combinatino to the ans array, and, we recurse, and then we backtrack (arr pop)


"""