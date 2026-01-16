print("Quick test")


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def print_tree_pretty(root, level=0, prefix="Root: "):
    """
    Prints tree with indentation showing structure
    """
    if root is not None:
        tabulation = " " * (level * 4)
        print(tabulation + prefix + str(root.val))
        if root.left is not None or root.right is not None:
            if root.left:
                # if current node has value, recurse and print
                print_tree_pretty(root.left, level + 1, "L--- ")
            else:
                # If current node does not have value, just print None
                print(" " * ((level + 1) * 4) + "L--- None")
            if root.right:
                print_tree_pretty(root.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")

class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:
        # What is our base case?
        if not root:
            return

        l = root.left
        r = root.right

        # We should reverse on each level
        if (root.left):
            root.left = r
        if (root.right):
            root.right = l
        

        # Keep going down
        self.invertTree(root.left)
        self.invertTree(root.right)
        
        return root


quickTree = TreeNode(4)
quickTree.right = TreeNode(7)
quickTree.left = TreeNode(2)
quickTree.left.left = TreeNode(1)
quickTree.left.right = TreeNode(3)
quickTree.right.left = TreeNode(6)
quickTree.right.right = TreeNode(9)


print_tree_pretty(quickTree)
# Calling our function
problem = Solution()
resNode = problem.invertTree(quickTree)
print_tree_pretty(resNode)

