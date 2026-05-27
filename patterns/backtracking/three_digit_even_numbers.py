"""
    You are given an integer array digits, where each element is a digit. The array may contain duplicates.

    You need to find all the unique integers that follow the given requirements:

    The integer consists of the concatenation of three elements from digits in any arbitrary order.
    The integer does not have leading zeros.
    The integer is even.
    For example, if the given digits were [1, 2, 3], integers 132 and 312 follow the requirements.

    Return a sorted array of the unique integers.

    

    Example 1:

    Input: digits = [2,1,3,0]
    Output: [102,120,130,132,210,230,302,310,312,320]
    Explanation: All the possible integers that follow the requirements are in the output array. 
    Notice that there are no odd integers or integers with leading zeros.
    Example 2:

    Input: digits = [2,2,8,8,2]
    Output: [222,228,282,288,822,828,882]
    Explanation: The same digit can be used as many times as it appears in digits. 
    In this example, the digit 8 is used twice each time in 288, 828, and 882. 
    Example 3:

    Input: digits = [3,7,5]
    Output: []
    Explanation: No even integers can be formed using the given digits.

"""
"""
    Brainstorm:
    - We need EVEN numbers constructed using 3 digits FROM the array
    - This array may contain duplicates, so we can/must use them as well
    - So this means my final array does NOT need to be odd
    - A number is even if the last digit is even, so 112 is even, for example
    - We need to create all combinations possible using the elements in the array (nested loops?)
    - Once we build the output, we need to SORT it (can I sort if once I finish building the array or can I do it as I build the array) 
    ...
"""
# Permutations: Possible combination
def findEvenNumbers(digits: list[int]) -> list[int]:
    digits.sort()
    final_result = []
    
    # Create all combination of 3 digits possible, how can I do this?
    for i in range(len(digits)):
        #print(f"current digit: {digits[i]}")
        if digits[i] != 0:
            for j in range(len(digits)):
                if i is not j:
                    for k in range(len(digits)):
                        if k is not i and k is not j:
                            # Generate all permutations
                            combination = digits[i] * 100 + digits[j] * 10 + digits[k]
                            print(combination)
                            if combination % 2 == 0:
                                last_element = final_result[-1] if len(final_result) > 0 else 0
                                if combination > last_element:
                                    final_result.append(combination)
                                
        
    return final_result

# remove index from our array
# pass the indices of i, j in the parameters
def generatePermutations(digits: list[int], current_length: int = 0, current_permutation: int = 0):

    if len(digits) == 0:
        return []

    if(current_length == 4):

        if current_permutation % 2 == 0:
            return [current_permutation]
        
        return []
    
    if(current_length == 1 and current_permutation == 0):
        return []
 
    result = set()

    for i in range(len(digits)):

        current_digit = digits[i]
        remainder = digits.copy() 
        del remainder[i]

        result = result.union(generatePermutations(remainder, current_length+1, current_permutation*10 + current_digit))

    return result




test_input = [2, 1, 3 ,0]
test_input_2 = [2,2,8,8,2]


res = generatePermutations(test_input_2)
print(f"FINAL RESULT: {res}")

#print("******" ,test_input[-1])
t = [2, 2, 2]
"""
    [2, 1, 3, 0]
    213, 210, 123, 210, 321, 312, 320, 310, 
"""
#res = findEvenNumbers(test_input_2)
#print(f"FINAL RESULT: {res}")



