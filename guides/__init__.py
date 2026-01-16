"""
Trees Module - Simple imports for binary tree practice

Usage:
    from trees import TreeNode, build_tree, printTree
    
    # Create and visualize a tree
    root = build_tree([1, 2, 3, 4, 5])
    printTree(root)
"""

# Core essentials
from .utils.tree_node import TreeNode
from .utils.tree_builder import build_tree
from .utils.tree_printer import printTree

# Traversals
from .traversal.preOrderTraversal import preOrderTraversal
from .traversal.inOrderTraveral import inOrderTraversal
from .traversal.postOrderTraversal import postOrderTraversal

# Cleaner aliases
preorder = preOrderTraversal
inorder = inOrderTraversal
postorder = postOrderTraversal

__all__ = [
    # Essentials
    'TreeNode',
    'build_tree',
    'printTree',
    
    # Traversals (both styles)
    'preorder',
    'inorder',
    'postorder',
    'preOrderTraversal',
    'inOrderTraversal',
    'postOrderTraversal',
]
