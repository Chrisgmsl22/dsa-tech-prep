class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        # Dont forget to consider checks for edge cases
        counter = 0 # See if we need this
        jCounter = {}
        sCounter = {}

        for j in jewels:
            jCounter[j] = jCounter.get(j, 0) + 1
        
        for s in stones:
            sCounter[s] = sCounter.get(s, 0) + 1
        
        # Go over each one and see if the current stone is present in jCounter
        print(jCounter, sCounter)
        for s in sCounter:
            if s in jCounter:
                counter += sCounter[s]
        
        return counter

""""
    NOTES:
    - Input: 2 args: jewels, which contains a string with all the stones that are jewels
        And stones, which contains a string of all the stones we have
    
    - Output: a number, which represents the amount of stones we have that are considered jewels
    - Things to consider: Our string is case sensitive, so a is not the same as A.

        Brainstorm approach:
        We need to compare the content of the 2 arguments given
        jewels will act as our source of truth, because we will use thm to identify the actual jewels

        And stones is going to be our target
        we need to go over the entire collection (iterations of some sort), but given that we need to count
        how many there are, this is a form of a frequency count.
        We need to obtain the frequency count for each argument and then start with stones

        We can have a counter that we can use, or we use this frequency count somehow

        in the end, we return our result after we have completed the iteration.

"""