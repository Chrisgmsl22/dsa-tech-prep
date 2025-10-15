"""
    Dada una matriz cuadrada de números enteros de tamaño n x n, debes calcular la suma de
    los números capa por capa (anillo por anillo), comenzando desde la capa exterior hasta llegar
    al centro de la matriz.
    Cada "capa" se define como el borde que rodea la matriz, y debes considerar:
    ●
    La fila superior de la capa
    ●
    La columna derecha de la capa (sin contar las esquinas ya sumadas)
    ●
    La fila inferior de la capa
    ●
    La columna izquierda de la capa (sin contar las esquinas ya sumadas)
    Al terminar de recorrer la matriz:
    ●
    Si n (el tamaño) es impar, habrá un único número en el centro de la matriz que deberá
    contarse como una capa adicional.
    Debes devolver una lista de enteros, donde cada posición representa la suma total de cada
    capa (en orden de afuera hacia adentro).
    
    Ejemplo
    Si la entrada es:
    [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
    ]
    El resultado debe ser:
    [8, 1]
    Explicación:
    ●
    La primera capa suma 8 (todos los bordes exteriores).
    ●
    El número central es 1.
"""

"""
    Brainstorm: 
    - squared matrix (so they have the same number of rows and columns)
    - size could be even or odd, based on this one layer/ring will be just one value
    - need to consider each corners, and then the number of elements between them (like a rubiks cube)
    - we need to start from the outside first, and then move up to the inside
    - Need to figure out a pattern or a formula to then just move inside UNTIL a certain condition is met (probably ring size, even or odd)
    - this function takes in a matrix, which is an array of arrays
    - This function returns an array, where its elements are the sum of all rings, and where each element is separated by a comma, where the next item is the next ring, and so on, until the end is reached
    - Need iterations,
    - Do we need a certain utils function???
"""
"""
    Plain english pseudocode:
    define function{
        temp_array to store all values within the CURRENT ring
        final_result to store all rings
        
        identify each corners (left to right) (right, to bottom) (bottom to left) (bottom to upper left)
        identify all elements within each pair of corners
        ***Find a pattern, so that we can define an algorithm
        
        perfom row iteration {
            perform cell iteration {
                # do the calculation here, which I am not too sure yet on how to do it
            }
        }
        
        return final_result
    }
"""

# DO NOT FORGET TO ADD SECURITY CHECKS ONCE YOUR FUNCTION HAS BEEN DEFINED
def sum_per_layers_in_matrix(matrix: list[list[int]]) -> list[int]:
    final_result = []
    
    while len(matrix) != 0:
        if len(matrix) == 1:
            final_result.append(matrix[0][0])
            del matrix[0]
            break
            
        temp = 0
        for i in range(len(matrix)):
            row = matrix[i]
            first_index = 0
            last_index = len(row) - 1
            print(f"Matrix before operations: {matrix}")
            print(f"Row: {i, row}")
               
            # if its first or last layer, then add all elements
            if i == first_index or i == last_index:
                temp += sum(row)
                row.clear()
            else:
                #otherwise, only add first and last elements
                temp += row[first_index] + row[last_index]
                row.pop()
                row.pop(0)
            
            
                
            print(f"temp: {temp}") # 16
        final_result.append(temp)
        
        # Delete empty arrays
        del matrix[0]
        del matrix[len(matrix) - 1]
        
    print(f"Matrix, after operations: {matrix}")   
    return final_result


# number of elements in total: 9, if its odd, then it has a single ring at the end
# if the number of elements is even, then it has a ring of 2x2
test = [[1]]
test_input_one = [
    [1, 1, 1], [1, 1, 1], [1, 1, 1] # [8, 1]
]
test_input = [ # [16, 1]
    [2, 2, 2],
    [2, 1, 2],
    [2, 2, 2]
]
test_input_two = [ # [24, 7]
    [2, 2, 2, 2],
    [2, 1, 2, 2],
    [2, 2, 2, 2],
    [2, 2, 2, 2]
]
#print(f"Before {test_input}")
#del test_input[0]
#print(f"After: {test_input}")
#print(f"Find center: {len(test_input) // 2}")
#print(f"Find center2: {len(test_input_two) // 2}")

"""
    if last ring is even, then add ALL items
    if last ring is odd, then just add that single item to the array
    [ 
        [1, 2, 3, 4, 5, 6], -> first layer will contain all items
        [1, 2, 3, 4, 5, 6], -> inner will only contain first and last
        [1, 2, 3, 4, 5, 6], -> inner will only contain first and last 
        [1, 2, 3, 4, 5, 6], -> inner will only contain first and last
        [1, 2, 3, 4, 5, 6], -> inner will only contain first and last
        [1, 2, 3, 4, 5, 6], -> last layer will contain all items
    ]
    [
        [1, 2, 3, 4], -> First layer will collect all items
        [1, 2, 3, 4], -> inner layer will only contain first and last items
        [1, 2, 3, 4], -> inner layer will only contain first and last items
        [1, 2, 3, 4] -> last layer will collect all items
        ------------
        [        ],
        [  2, 3  ],
        [  2, 3   ],
        [         ]
    ]

    [
        [X, 1, X], -> first iteration, first and last elements will be our point of reference
        [1, 1, 1], -> For now we dont need to find certain indices here*
        [X, 1, X] -> third iteration, first and last elements will be our point of reference
    ]
"""
res = sum_per_layers_in_matrix(test)
print(f"FINAL RESULT {res}")