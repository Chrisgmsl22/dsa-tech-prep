class Solution:
    def reverseStr(self, s: str, k: int) -> str:
        sArr = list(s) # Easier to handle when dealing with strings
        n = len(sArr)
        def reverse(a: int, b: int) -> None:
            while a <= b: # Ideally should be l and r
                sArr[a], sArr[b] = sArr[b], sArr[a]
                a += 1
                b -= 1
        # Reverse all

        # Reverse first k
        # a b c d e f g==> k = 2 ==> EXPECTED: 
        #         i  
        # ba  cd

        i = 0
        # Normal flow
        while i < n:
            # Ask if there is at least k -1 upfront to flip (2 - 1 = 1)
            chunk = (i + k) - 1
            windowSize = ((n - 1) - i) + 1
            if chunk in range(n):
                reverse(i, chunk) # Reverse first k chars for every 2k
            elif windowSize < k:
                print('reverse all')
                reverse(i, n - 1)
                break
            elif windowSize >= k and windowSize < (2 * k):
                # reverse first k
                reverse(i, chunk)

            i += (k * 2) # step is K times

        
        return "".join(sArr) 





"""
    NOTES:
    - Input: A string, which may contain repeated characters?, and a target K
    - Output: a new string, which represents the reversed string where we only reverse the first k characters

    Things to be aware of: We need to make sure we do every 2k characters, do they mean 2,000?, or 2 * k ?, will probably need to have a test case break my code just so I can understand the desired output.

    If len(s) < 2,000 BUT >= k, reverse the first k and leave the other as original (like the first 2 examples of the test)
    Still need to watch out for the 2 edge cases described here

    Ohh, so every 2 steps, we want to flip them?


"""