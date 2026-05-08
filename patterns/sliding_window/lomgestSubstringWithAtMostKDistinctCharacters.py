"""
 Given a string s and integer k, return the length of the longest substring that contains at most K distinct
  ▎ characters.

Examples:
  - s="eceba", k=2 → 3 (the substring "ece")
  - s="aa", k=1 → 2
"""

class Solution:
    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        L = 0
        ans = 0
        freqCounter: dict[str, int] = {}
        n = len(s)
        # e c e b a ==> k = 2
        #     L
        #       R
        # {e: 1, b: 1}

        for R in range(n):
            currChar = s[R]
            freqCounter[currChar] = freqCounter.get(currChar, 0) + 1

            # Validate: While our current window is invalid, shrink
            while len(freqCounter) > k:
                leftmostChar = s[L]
                freqCounter[leftmostChar] -= 1
                if freqCounter[leftmostChar] == 0:
                    del freqCounter[leftmostChar]
                
                L += 1

            # Ok, window is valid
            windowSize = (R - L) + 1
            ans = max(ans, windowSize)

        return ans


sol = Solution()
s = "eceba"
k = 2

res = sol.lengthOfLongestSubstringKDistinct(s, k)
print(res)


""""
    Input: a string which may contain repeated characters, and an integer K
    - Output: a number, which represents the length of the LONGEST substring with at most K distinct characters.

    Basically, what we need to do, is to build up a substring, and the constraint is that the substring may contain at most K unique characters. So "eec" k = 2 is valid, length is 3, but chars are 2.
    But "aabc" k=2 is not valid, length is 4, but total chars are 3

    Assumptions: our string contains only lowecase english letters. Can it be empty?, Ks value can be 0?, can K > len(s)?

    Initial approach:
        We need to build up a substring, for this we will use pointers, L and R. these 2 will tell us our exact window size.
        So we need to be able to increase it as we go.
        When do we shrink the window? When the total chars in the substring are greater than K, window is invalid so we shrink.
    
        We may have different answers across the whole algorithm, so we will need to keeo track of it.

        Mental model: Sliding window, IEAVRR: Initialize, Expand, Add, Validate, Remove, Record
"""