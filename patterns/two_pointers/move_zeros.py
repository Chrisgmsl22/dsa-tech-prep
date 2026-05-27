"""
    Ejercicio 1: Move Zeroes (Fácil)
    Enunciado:
    Dado un array de enteros, mueve todos los ceros al final manteniendo el orden relativo del resto de los elementos en lugar (sin usar otro array).

    # Ejemplo:
    # Input:  [0,1,0,3,12]
    # Output: [1,3,12,0,0]
    Intenta implementarlo usando dos punteros, donde uno va manteniendo el lugar donde debería ir el siguiente número distinto de cero.


"""

"""
    - Notes:
    - two pointer approach, we need one pointer who will run through the whole array
    - second pointer will keep track of where the numbers different than zero will go
    - we go left to right? (consider right as well)
"""

class MoveZeroes:
    def __init__(self):
        pass
    def moveZeroes(self, arr: list[int]) -> list[int]:
        #  [1,3,12,0,0] ir current num == 0, then just move, if not, then swap (both) and increase left and right
        #.         l 
        #.              r iteration finishes
        left: int = 0
        
        for right in range(len(arr)):
            currentNum = arr[right]
            if currentNum != 0:
                # Swap values (a, b = b, a)
                arr[left], arr[right] = arr[right], arr[left]
                left += 1
                #right += 1
            print('Current state of my array: ', arr)
    
    
solution = MoveZeroes()
testInput = [0,1,0,3,12]
testInput2 = [1,2,0,0,14,0,20] # [1,2,14,20,0,0,0]

res = solution.moveZeroes(testInput2)

#print(res)