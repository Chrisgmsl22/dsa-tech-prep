"""
    Palindrome Check

    👉 Check if a string is a palindrome.
    Example: "racecar" → True, "hello" → False

    Recursive Breakdown

    Base case: String length ≤ 1 → True.

    Recursive case: First and last chars must match AND middle substring must also be a palindrome.

"""
def isPalindrome(word: str) -> bool:
    # Base case goes here
    if len(word) <= 1: return True # We've chopped the whole word, it is valid

    # If not, lets make sure both opposite ends are equal
    firstChar = word[0]
    lastChar = word[-1]

    if firstChar != lastChar:
        # If they're not the same, then its not a palindrome
        return False
    
    # Connect the call stack
    reducedWord = word[1 : -1] # Start from the second char up to one before the last one
    return isPalindrome(reducedWord)


print(isPalindrome("aa"))

    # recursion call