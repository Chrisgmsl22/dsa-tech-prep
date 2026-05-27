class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        # We might need security checks for empty words, etc ...
        res = ""

        p1, p2 = 0, 0

        # a b c
        #     1
        # p q r D D
        #     2
        # a p b q c r
        while p1 < len(word1) and p2 < len(word2):
            # We first grab the first character
            res += word1[p1]
            p1 += 1

            res += word2[p2]
            p2 += 1
        # After this we stop iterating
        if len(word1) > len(word2):
            # Then one is larger
            res += word1[p1 :]
        else:
            res += word2[p2 :]
        
        return res

    def mergeAlternately2(self, word1: str, word2: str) -> str:
        res = ""
        minL = min(len(word1), len(word2))

        # We fill up to the shortest word (because it will be contained within both)
        for i in range(minL):
            res += word1[i]
            res += word2[i]
        
        # Lets check in case we have values left
        if len(word1) > len(word2):
            res += word1[minL :]
        elif len(word2) > len(word1):
            res += word2[minL :]
        
        return res
"""
    NOTES:  
    - Input: 2 strings, w1 and w2
    - Output: A single string, which contains both words added character by character 
    in alternating order
        If a string ends up being longer than the other, then by the time we reach
        the end of the shortest one, we append all the rest of the letter to the final word
    
    Brainstorming:
        We need to iterate over the 2 words, we cannot do for loops because they will
        run continuously, so there would not be a way for us to pause them
        So my second thought is to use a while loop for each word (maybe?), 
        and have this while loop working with pointers

        While p1 and p2 are not at the end
        then grab p1s character and add it to a final word
        then grab p2s character and add it to the final word

        Keep track of the length, because if one of them ends, or if the pointer is at the
        end of the word but the other still continues, then we need to add the rest

        by the time youre done, just return the final word
"""