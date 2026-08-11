class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        counter = 0

        for s in stones:
            if s in jewels:
                # Then its a valid new jewel
                counter += 1
        return counter



"""
    NOTES:
    - Input: 2 strings, which represent the jewels available, and the stones I have
    - Output: number, which represents how many stones that I have are also jewels.

    The main thing here is that each character is case sensitive, meaning that a is different from A.
    So as a result we treat them as different characters.

    Brainstorm approach:
    We, need to define what is a valid jewel. And this will be our source of truth.
    Once we have this, we need to go over all of out stones and check if our current is part of this
    If it is, then we have a jewel, so we increase a counter, or collect this value somehow.

    If we happen to find the same stone being the same jewel and we already collected it, we ignore it
    Since we care about new jewels.

    We can use a hashMap to define the different jewels, an maybe another hashMap for our current stones.
    or even a set, so we reduce repeated values.

"""
