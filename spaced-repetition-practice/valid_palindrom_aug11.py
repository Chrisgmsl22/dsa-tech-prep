class Solution:
    def isPalindrome(self, s: str) -> bool:
        clean = ""

        for char in s:
            char = char.lower()
            if char.isalnum():
                clean += char
        # Once word is clean, we now define our code to check if its a palindrome
        L, R = 0, len(clean) - 1

        while L < R:
            if clean[L] != clean[R]:
                #print("Not valid, ", L, R, s[L], s[R])
                return False
            L += 1
            R -= 1

        return True



"""
    NOTES:
    - Input: a string, which contains a sentence (includes spaces)
    - Output: boolean, which represents the result of checking if the trimmed word is a palindrome
        A palindrome is a word that can be read the same forwards vs backwards

    Our string can be very big, so we need to make this efficient
    s, contains only ASCII characters

    We need to cleanup our string first.
    We need to trim it from spaces and make it all lower case
    Once its done, we can iterate over the string and compare both their ends
    if L == R, we're good, we continue
    once L and R are not equal, its when we know its not a valid word, no need to finish iteration, we can BREAK

    After the iteration, if we didnt break inside, it means we have a valid word, we return True

"""
