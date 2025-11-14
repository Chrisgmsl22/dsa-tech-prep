from traversal.preOrderTraversal import preOrderTraversal
from classes.tree import TreeNode
from utils.printTree import print_tree_pretty







# Create the tree
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)
root.right.left = TreeNode(10)


print_tree_pretty(root)
print(preOrderTraversal(root))