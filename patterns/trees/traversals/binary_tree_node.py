# Definition for a binary tree node.

class Node:
    def __init__(self, val = 0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right
        
root_node = Node(1)
root_node.left = Node(2)
root_node.right = Node(3)

root_node.left.left = Node(4)
root_node.left.right = Node(5)

# Example Tree:
#       1
#      / \
#     2   3
#    / \
#   4   5

result = []
def in_order_traversal(node: Node) -> list[int]:
    if node is None: 
        return
    
    
    in_order_traversal(node.left)
    print(node.val, end=" ")
    result.append(node.val)
    in_order_traversal(node.right)
    
    return result


res = in_order_traversal(node=root_node)
print(f"Final result: {res}")