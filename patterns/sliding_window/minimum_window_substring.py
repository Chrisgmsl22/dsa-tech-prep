""" 
    Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".

The testcases will be generated such that the answer is unique.


Example 1:

Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.
Example 2:

Input: s = "a", t = "a"
Output: "a"
Explanation: The entire string s is the minimum window.
Example 3:

Input: s = "a", t = "aa"
Output: ""
Explanation: Both 'a's from t must be included in the window.
Since the largest window of s only has one 'a', return empty string.

""" 
class Solution:
    def isCurrWindowValid(self, t: str, freq: dict[str, int]) -> bool:
        # lets turn t into a freqCount as well.
        tMap: dict[str, int] = {} 
        for c in t:
            tMap[c] = tMap.get(c, 0) + 1
        print("tMap: ", tMap) # {a: 2}
        for key in tMap.keys():
            print("Is key present in freq: ", (key not in freq))
            if key not in freq:
                return False
            print("key counter is less than freq?: ", (tMap[key] < freq[key]), tMap[key], freq[key])

            if freq[key] < tMap[key]:
                return False
        
        return True


    def minWindowOld(self, s: str, t: str) -> str:
        L = 0
        freqCount: dict[str, int] = {}
        ans = ""
        n = len(s)
        # a a || t = "aa"
        # L
        # R
        # {a: 1}
        for R in range(n):
            currChar = s[R]
            freqCount[currChar] = freqCount.get(currChar, 0) + 1

            # If invalid shrink
            while self.isCurrWindowValid(t, freqCount):
                # We're going to try to shrink, but first, store valid window
                possible = s[L : R + 1]
                if not ans or (len(possible) < len(ans)):
                    # Then we found a smaller one
                    ans = possible

                leftmostChar = s[L]
                freqCount[leftmostChar] -= 1
                if freqCount[leftmostChar] == 0:
                    del freqCount[leftmostChar]
                L += 1


            # Once all chars are included, we capture curr min
            # If T's chars are included in freqCount? ...

            
            # update
        return ans

    def minWindow(self, s: str, t: str) -> str:
        L = 0
        freqCount: dict[str, int] = {}
        ans = ""
        have = 0

        tMap: dict[str, int] = {}
        for char in t:
            tMap[char] = tMap.get(char, 0) + 1
        
        need = len(tMap)
        # A D O B E C O D E B A N C ====== ABC => {A: 1, B: 1, C: 11}
        # L
        #           R
        # have: 3
        
        for R in range(len(s)):
            currChar = s[R]
            freqCount[currChar] = freqCount.get(currChar, 0) + 1

            # increment have
            if (currChar in tMap) and (freqCount[currChar] == tMap[currChar]):
                have += 1

            while have == need:
                currWindowSize = (R - L) + 1
                if not ans or currWindowSize < len(ans):
                    ans = s[L : R + 1]

                # Capture and shrink
                leftChar = s[L]
                if (leftChar in tMap) and (freqCount[leftChar] == tMap[leftChar]):
                    have -= 1
                
                # Shrink window by default
                freqCount[leftChar] -= 1
                if freqCount[leftChar] == 0:
                    del freqCount[leftChar]
                
                L += 1
            
        return ans

sol = Solution()

s = "ADOBECODEBANC" 
t = "ABC"
# Expected res: BANC
s2 = "aa"
t2 = "aa"

res = sol.minWindow(s, t)

print("Final result: ", res)

"""
    NOTES:
    - Input: 2 strings, s and t. S seems to be larger than T
    - Output: A string, which represent the MINIMUM window (smallest possible) where T is contained within the substring
    created from S. If there is no answer, we can return an empty string.

    - Assumptions: Will our strings always have a value?, can T be larger than S?, does it only contain english characters?

    This is a sliding window problem, our goal is to form a substring that contains all of the characters from T.
    A substring is created from S and we can use a pointer to start defining the window sizes
    We need to know what if the elements from T are included in the current substring.
    How do we do that?, right now I can only think of iteration over a hashMap or something like that.

    If window is valid, then capture the curr Ans, the final result should the the SMALLEST window, so ideally we need to shrink the window and see how valid it is, if we remove it and it turns out to be invalid, then we keep growing the window until we reach the end.

    Framework for sliding window: Initialize (L, windowState, ans), Expand, Add to windowState, Validate, Remove and Record.

"""