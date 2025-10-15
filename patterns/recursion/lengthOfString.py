"""
    Problem 5: Length of a String

Find the length of a string without using len().

Hint:

Base case → empty string.

Recursive step → count 1 + recurse on substring without the first char.
"""
class Recursion:
    def findLength(self, s: str, counter = 0) -> int:
        # Identify base case
        if s == "":
            return 0 # Break
        
        # Identify recursion case
        return counter + 1 + self.findLength(s[ : -1], counter)
        
    

inputData = "hello"
solution = Recursion()
res = solution.findLength(inputData)

print(res)