"""
    Reverse a string recursively
    Input: "hello"

    Output: "olleh"
    
    h e l l o
    
    o + (fn("hell"))
    o + l + (fn(hel))
    o + l + l + (fn(he))
    o + l + l + e + (fn(h))
    
    o + l + l + e + h
    olleh
"""

class Recursion:
    def __init__(self):
        pass
    def solution(self, word: str) -> str:
        # Base case: if the string is empty, or is just 1, then its already reversed, return it
        if len(word) <= 1:
            return word

        # Recursive case
        restReversed = self.solution(word[1:])
        return restReversed + word[0]
    
    def reverseString(self, s: str, call_stack = []) -> str:
        
        call_stack.append(f"reverseString('{s}')")
        print(f"Call stack: {' -> '.join(call_stack)}")
        # Identify base case
        if len(s) <= 1:
            return s
        
        # Identify recursion case
        # take the last character PLUS recurse on the rest
        lastChar = s[-1]
        remaining = s[0 : len(s)  ]
        return lastChar + self.reverseString(remaining)

    def reverseString2(self, s: str) -> str:
        # Identify base base
        if len(s) == 1:
            return s
        
        left, right = s[0], s[-1]
        return right + s[1 : -1] + left
        
        # Identify recursion case   
        

word = "hello"
recInstance = Recursion()
print(recInstance.reverseString2(word))

