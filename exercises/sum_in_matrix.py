"""
    You are given a 0-indexed 2D integer array nums. Initially, your score is 0. Perform the following operations until the matrix becomes empty:

From each row in the matrix, select the largest number and remove it. In the case of a tie, it does not matter which number is chosen.
Identify the highest number amongst all those removed in step 1. Add that number to your score.
Return the final score.

 

Example 1:
7 + 6 + 6 + 3 +> 7
2 + 4 + 5 + 2 => 5
1 + 2 + 3 + 1 => 3
= 15 This is only valid, if our matrix is empty
[[], [], []]
Input: nums = [[7,2,1],[6,4,2],[6,5,3],[3,2,1]]
Output: 15
Explanation: In the first operation, we remove 7, 6, 6, and 3. We then add 7 to our score. Next, we remove 2, 4, 5, and 2. We add 5 to our score. Lastly, we remove 1, 2, 3, and 1. We add 3 to our score. Thus, our final score is 7 + 5 + 3 = 15.
Example 2:

Input: nums = [[1]]
Output: 1
Explanation: We remove 1 and add it to the answer. We return 1.

"""

"""
    brainstorm: matrix 2D => nested loops (2 times, at least), find the largest (comparison, do I need another loop? is there a built in PY function that can help me make my life easier?).
    
    we need to sum all results from each iteration, -> I might need an array to store this[]
    
    we STOP until the matrix is empty? (would I need a while loop)**
    
    output will be a number
"""

"""
    plain english:
    
    define the function:
    define array* to store result from each iteration
    comparison, this will contain the largest one from this iteration***
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    iterate over rows:
        <><>
        iterate over columns:
            #what do we do here?
    
"""
import sys
def sum_in_matrix(matrix: list[list[int]]) -> int:
    final_result_array = []
    # lets do the outer iteration
    
    while len(matrix[0]) > 0:
        current_max_values = []
        for i in range(len(matrix)):
            row = matrix[i]
            print(f"Row: {row}")
            
            temp = -sys.maxsize
            for j in range(len(row)):
                cell = row[j] #matrix[i][j]
                if cell > temp:
                    temp = cell # im going to give it the index
            # continue the logic, we need to remove the largest one, from the array
            row.remove(temp)
            current_max_values.append(temp)
            
        final_largest_value = max(current_max_values)
        final_result_array.append(final_largest_value)
        
        
        print(f"Current state of matrix: {matrix}")
        print(f"current_max_values length: {current_max_values}")
    return sum(final_result_array)
                
            
            
        
test_input = [[1, 2, 3],[4, 5, 6],[7, 8, 9]]
test_input_two = [[7,2,1],[6,4,2],[6,5,3],[3,2,1]] # Expectec outcome: 15
test_input_three = [[-7,-2,-1],[-6,-4,-2],[-6,-5,-3],[-3,-2,-1]]
"""
    [
        [-7, -2, -1], 
        [-6, -4, -2], 
        [-3, -2, -1] 
    ]
    
"""
res = sum_in_matrix(test_input_three)
print(f"FINAL RESULT: {res}")
#print()
test = [[], [], []]

test_2 = []
#print(len(test[0]))