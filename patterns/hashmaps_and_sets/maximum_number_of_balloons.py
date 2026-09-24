class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        charCount: dict[str, int] = {}
        balloons = 0 # Our final answer
        balloonKeys: dict[str, int] = {"b": 1, "a": 1, "l": 2, "o": 2, "n": 1}
        # Populare our word counter
        for char in text:
            charCount[char] = charCount.get(char, 0) + 1
        # loonbalxballpoon
        # {'l': 4, 'o': 4, 'n': 2, 'b': 2, 'a': 2, 'x': 1, 'p': 1}
        #print(charCount)
        # Need to traverse through our map, see if we have enough chars
        while "b" in charCount: # All chars need to be in, but we could use this one to start with
            for key in balloonKeys.keys():
                if key not in charCount or charCount[key] < balloonKeys[key]:
                    return balloons
                # Otherwise, reduce current char
                charCount[key] -= 1
                if key == "l" or key == "o":
                    charCount[key] -= 1

                if charCount[key] == 0:
                    del charCount[key]
            # By this point we should have formed our full word, so we increase our counter
            balloons += 1
            
        
        return balloons


"""
    NOTES:
    - Input: A string of characters, only english lowercase letters
    - Output: Number, which represents the total amount of "balloon" words we can form by consuming the chars
    We cannot reuse existing characters, so once we found a valid word, we cannot reuse those chars again
    If we do not find a word in the whole string, we simply return zero.


    We need to be aware of the total number of characters we have, for this we can use a char counter
    Next, we need to know what the word "balloon" represents in the counter.
    {b: 1, a: 1, l: 2, o: 2, n: 1}, this is how much it takes to form a word that says balloon.

    We need to make sure our current counter has at least this amoung of counts before increasing our "word found" counter.
    If at least one is not present, then its not valid

    By the time our algorithm finishes, then we must have found our solution

"""