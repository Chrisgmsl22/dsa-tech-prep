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


Follow up: Suppose there are lots of incoming s, say s1, s2, ..., sk where k >= 109, and you want to check one by one to see if t has its subsequence. In this scenario, how would you change your code?
"""
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        sP, tP = 0, 0
        # counter == len(S) then true
        # s -> A B C
        #      i
        # t -> A H B G D C
        #      i
        while tP < len(t):
            currTChar = t[tP]
            currSChar = s[sP]

            if currTChar == currSChar:
                sP += 1
                print(sP, 'Values match', currSChar, currTChar)
            tP += 1

        return sP == len(s)
sol = Solution()
s = "abc"
t = "ahbgdc"

res = sol.isSubsequence(s, t)

print("OUTCOME: ", res)

"""
    NOTES:
        - Input: 2 strings, which can be very large
        - Output: boolean value, which represents the result of checking if S is a subsequence of T

        What is a subsequence: A subsequence is a resulting string (in this case) that can be formed by deleting (or not) characters from our original variable. The thing to evaluate here is that T needs to keep the same order of their characters.

        ABCDE s
        AE is a subsequence, because eventhough we removed characters, A and E follow the natural order as ABDCE

        EA is not a sequence, because the order is reversed.

        Ok, we need two pointers, because we need to keep track of the position of our current characters in their corresponding words.
        We need to be careful with not going overflow

        We compare each one, and we use T as our target.
        If we have seen it in the correct order, we simply continue

        How do we know when its not valid?, could be when we have not seen a character and we already found another char?
"""
