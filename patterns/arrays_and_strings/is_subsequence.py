""" 
Given two strings s and t, return true if s is a subsequence of t, or false otherwise.

A subsequence of a string is a new string that is formed from the original string by deleting some (can be none) of the characters without disturbing the relative positions of the remaining characters. (i.e., "ace" is a subsequence of "abcde" while "aec" is not).

 

Example 1:

Input: s = "abc", t = "ahbgdc"
Output: true
Example 2:

Input: s = "axc", t = "ahbgdc"
Output: false
 

Constraints:

0 <= s.length <= 100
0 <= t.length <= 104
s and t consist only of lowercase English letters.


""" 
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        # Let's consider edge cases
        S, T = len(s), len(t)
        if not s: return True
        if S > T: return False

        ps = 0 # s pointer

        # We will iterate over t string, which is our source of truth
        for i in range(T):
            if t[i] == s[ps]:
                if ps == S - 1: # Avoid overflow 
                    return True 
                ps += 1
        

        return False



s = "abc"
t = "ahbgdc"

sol = Solution()
print(sol.isSubsequence(s, t))
#print(sol.isSubsequence("b", "abc"))