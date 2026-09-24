class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        n = len(s)
        longest = 0
        l = 0
        charCount = {}
        # A A B A B B A ==> k: 1
        # l
        #       r
        # unique: A
        # longest: 4
        # ops: 1 
        # Counter: {A: 3, B: 1}
        for r in range(n):
            currChar = s[r]

            # Add char to counter
            charCount[currChar] = charCount.get(currChar, 0) + 1
            
            #print("Current state of dict: ", charCount)
            # window size - biggest Counter = replacements needed
            while ((r - l) + 1) - max(charCount.values()) > k:
                # Shrink
             #   print(l, s[l])
                leftC = s[l]
                charCount[leftC] -= 1
                if charCount[leftC] == 0:
                    del charCount[leftC]
                l += 1

            windowSize = (r - l) + 1
            longest = max(longest, windowSize)
        
        return longest


"""
    NOTES:
    - Input: a string, which contains only UPPERCASE english characters and a number, which represents how many operations we can perform at most
    An operarion is the act of switching the current letter to be another one
    - Output: A number, which represents the longest substring that contains a repeated character with at most k operations.

    Ive seen this pattern before, I should not focus on performing actual operations but rather keep some sort of counter and mimmick 
    or assume my letter has the same value of my current substring.

    This is a sliding window, we start a window, and keep track the biggest value so far. 
    When we run into a letter different then the one from our current window, we increase a counter and assume its the same type.
    When do we shrink?, hmm, could be when we ran out of unique characters, we need to start shrinking, and thus reduce our counter as well

    Still need to polish the idea

    STOP labeling characters

"""