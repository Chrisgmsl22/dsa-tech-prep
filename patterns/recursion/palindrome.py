"""
    Palindrome Check

    👉 Check if a string is a palindrome.
    Example: "racecar" → True, "hello" → False

    Recursive Breakdown

    Base case: String length ≤ 1 → True.

    Recursive case: First and last chars must match AND middle substring must also be a palindrome.

"""
class Recursion:
    def isPalindrome(self, s: str) -> bool:
        # Identify base case
        if len(s) <= 1: return True
        
        topChar = s[-1]
        first = s[0]
        
        if topChar != first: return False
        
        return self.isPalindrome(s[1 : -1])
    

inputData = "racecar"
solution = Recursion()

print(solution.isPalindrome(inputData))