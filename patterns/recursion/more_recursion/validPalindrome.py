class Solution:
    def isPalindrome(self, s: str) -> bool:
        
        arr = [char.lower() for char in s if char.isalnum()]
        cleanString = "".join(arr)

        def recurse(s: str):
            print(s, len(s))
            if len(s) <= 1: return True
            if s[0] != s[-1]: return False

            return recurse(s[1 : -1]) # Slicing takes O(n) time, so time complexitt is n2

        return recurse(cleanString)
    def isPalindrome2(self, s: str) -> bool:
        alphaNumArr = [char.lower() for char in s if char.isalnum()]
        cleanString = "".join(alphaNumArr)

        def recurse(s: str, l: int, r: int):
            print(s, l, r)
            
            if l >= r: return True
            if s[l] != s[r]: return False # Comparison is constant
            #if len(s) < 2: return False

            return recurse(s, l + 1, r - 1) # Roughly n/2 calls, so Big O N
        
        return recurse(cleanString, 0, len(cleanString) - 1)
        


problem = Solution()
inputData = "racecar"
inputData2 = "A man, a plan, a canal: Panama" 

print(problem.isPalindrome2(inputData))