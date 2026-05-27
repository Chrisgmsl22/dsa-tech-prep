"""
A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.

 

Example 1:

Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.
Example 2:

Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.
Example 3:

Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.



"""
class Solution:
    def isPalindrome(self, s: str) -> bool:
        # Don't forget to account for edge cases once impl is done

        # First, we need to iterate over each character, and add it to an array if its alphanumeric, then we turn it into a string
        string = "".join([char for char in s if char.isalnum()]).lower()
        L, R = 0, len(string) - 1

        while L < R:
            leftmostChar = string[L]
            rightmostChar = string[R]

            if leftmostChar != rightmostChar:
                return False
            # Otherwise, continue
            L += 1
            R -= 1
        
        return True


sol = Solution()

s = "A man, a plan, a canal: Panama"
b = " "
print(sol.isPalindrome(b))

""""
    NOTES:
    - Input: a string, which represents a collection of alpanumeric characters and non-alpha numeric characters
    - Output: Boolean, which represents if a string is a palindrome, meaning it can be read the same forward and backward
    - Assumptions: Our string can contain non-alphanumeric characters, our string could contain at least 1 character and 
    it can be very large (so be careful with memory usage)


    Initial approach:
        Easiest way to check if a string is a palindrome is by reverting it, we can achieve this by reversing the string and 
        asking if the strings match, reversing by slicing, reversing by 2 pointers. So let's stick to a 1 pointer approach.
        Our current challenge is going to have to be removing the non alphanumeric characters, so how can we do this?

        Once its been trimmed, we can reverse it and be checking.


"""