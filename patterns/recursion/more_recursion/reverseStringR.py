class Solution:
    def reverseString(self, s: list[str], l: int, r: int) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        # What is going to be out base case?
        #print(s)
        if l >= r:
            return # Stop recursion

        # Swap
        s[l], s[r] = s[r], s[l]

        self.reverseString(s, l + 1, r - 1)




problem = Solution()
inputData = ["h", "e", "l", "l", "o"]

print(f"input data before: {inputData}")
res = problem.reverseString(inputData, 0, len(inputData) - 1)
print(res)
print(f"input data after: {inputData}")