
        

""" 
        brainstorm session: strings, arrays (keep in mind methods), loop/iterate (for loops)
        update values on every iteration, string.methods(), indices to check on each position of the array
        ...



        function that takes in an array of strings
        var longestPrefix = ""
        var currentWord = ""


        iterate over the array {
            FLOWER
            iterate over c {
                currentWord = c
                make sure this character is or is not present in currentWord
            }

            check IF the current stored word is also present in the next iteration

        }

        we return a string 
        
"""

""""
    FINAL RESULT: ...
"""
# self, str, classes
class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        longestPrefix = ""
      
        i = 0
       
        nth_character = strs[0][i]
        counter = 0


        # First iteration
        for index, word in enumerate(strs):
           
            print(index, word[0])
            if word[i] == nth_character:
                counter += 1
            
        if counter == len(strs):
            longestPrefix += nth_character
            i += 1
           
              
        return longestPrefix
            

# Duplicate code (STARTS WITH)
def longestCommonPrefix(arr: list[str]) -> str:
    longest_prefix = ""
    counter = 0
    
    first_word = arr[0]
    # Theoretically, the longest prefix can be the total length of the current word, so we need to iterate over the whole array n amount of times as long as its a valid prefix
    for k in range(len(first_word)): # for now we will go for the shortest word
        possible_prefix = first_word[:k + 1] # Consider that slicing 0 will return you nothing, so make sure you start at one
        print(f"Possible prefix: {possible_prefix}")
        for i in range(len(arr)):
            
            print(f"Current word: {i, arr[i]}")
            if arr[i].startswith(possible_prefix):
                counter += 1
        
        if counter == len(arr):
            longest_prefix = possible_prefix
            
        else:
            break
    
        counter = 0
        
                
    
    return longest_prefix
        
arr = ["flower","flow","flight"]
test_two = ["flow", "flower", "flowers"]
test_three = ['fl', 'flo', 'flos']

# Should assign its return to a variable
res = longestCommonPrefix(test_two)
print(f"FINAL RESULT: {res}")

"""
    But they key thing I recommend for you to do is this: 
    1.⁠Figure out how to determine that the first letter is the same for all words in your input, once you’ve done that then
    2.⁠⁠Figure out how to determine that the first two letters are the same for all words in your input, then
    3.⁠⁠Figure out how to determine that the 3rd letter isn’t the same for all words in your input
    
    arr[0][0]

"""
var = "flower"
print(f"SLICING: {var[:0 + 1]}")