"""
    Given a string s and a character c, count how many times c appears
    
    Example: "banana", "a" -> 3
"""
class RecursionClass:
    def countOcc1(self, s: str, c: str) -> int:
        # Identify base case
        if len(s) == 0:
            # It means we have an individual char
            return 0
        elif len(s) == 1:
            return 1 if s == c else 0
        
        # Identify recursion
        lastChar = s[-1]
        remaining = s[:-1]
        
        currentCount = 1 if lastChar == c else 0
        restCount = self.countOcc(remaining, c)
        return currentCount + restCount
   
    def countOcc(self, s: str, c: str) -> int:
        # Always consider base cases first 
        if len(s) == 0: return 0
        if len(s) == 1:
            if s == 1: 
                return 1 
            else: 
                return 0
        topElement = s[-1]
        remainingElements = s[ : -1]
        
        currentCount = 1 if topElement == c else 0
        remainingCount = self.countOcc(remainingElements, c)
        return currentCount + remainingCount
solution = RecursionClass()
input = "banana"
char = "a"
res = solution.countOcc(input, char)

print("res: ", res)