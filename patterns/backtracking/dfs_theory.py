# ===================================
# UNDERSTANDING DFS WITH DECISION TREES
# ===================================

print("DFS = Depth-First Search")
print("For subsets of [1, 2], we have this decision tree:")
print()
print("                    []")
print("                   /  \\")
print("              include    exclude")
print("                 1         1")
print("                /         /")
print("            [1]          []")
print("           /  \\         /  \\")
print("      include exclude include exclude")
print("         2      2       2      2")
print("        /      /       /      /")
print("    [1,2]   [1]      [2]    []")
print()
print("DFS visits nodes in this order: [], [1], [1,2], [1], [], [2], []")

# ===================================
# BASIC DFS TEMPLATE (The Foundation)
# ===================================

def dfs_template(current_state, remaining_choices):
    """
    This is the core DFS pattern you'll use everywhere!
    """
    print(f"Visiting: {current_state}")
    
    # BASE CASE: No more choices to make
    if not remaining_choices:
        print(f"  → Leaf reached: {current_state}")
        return
    
    # Get the next choice to consider
    next_choice = remaining_choices[0]
    rest_choices = remaining_choices[1:]
    
    # EXPLORE both options for this choice
    print(f"  → Deciding about: {next_choice}")
    
    # Option 1: Include the choice
    print(f"    Trying: INCLUDE {next_choice}")
    current_state.append(next_choice)  # Make the choice
    dfs_template(current_state, rest_choices)  # Go deeper
    current_state.pop()  # Undo the choice
    
    # Option 2: Exclude the choice  
    print(f"    Trying: EXCLUDE {next_choice}")
    # current_state stays the same
    dfs_template(current_state, rest_choices)  # Go deeper

print("\n" + "="*50)
print("BASIC DFS EXPLORATION OF [1, 2]:")
print("="*50)
dfs_template([], [1, 2])

# ===================================
# DFS WITH RESULT COLLECTION
# ===================================

def dfs_collect_results(elements):
    """DFS that actually collects all the subsets"""
    all_subsets = []
    current_subset = []
    
    def dfs(index):
        """
        index = which element we're currently deciding about
        """
        # BASE CASE: We've made decisions about all elements
        if index == len(elements):
            # We've reached a leaf - save this subset
            all_subsets.append(current_subset[:])  # Save a COPY
            return
        
        # RECURSIVE CASE: Decide about elements[index]
        current_element = elements[index]
        
        # Choice 1: INCLUDE current element
        current_subset.append(current_element)
        dfs(index + 1)  # Recurse to next element
        current_subset.pop()  # Backtrack
        
        # Choice 2: EXCLUDE current element
        # (current_subset unchanged)
        dfs(index + 1)  # Recurse to next element
    
    dfs(0)  # Start with the first element (index 0)
    return all_subsets

print("\n" + "="*50)
print("DFS COLLECTING ALL SUBSETS OF [1, 2, 3]:")
print("="*50)
subsets = dfs_collect_results([1, 2, 3])
for i, subset in enumerate(subsets):
    print(f"Subset {i+1}: {subset}")

# ===================================
# DFS WITH DETAILED TRACING
# ===================================

def dfs_with_trace(elements):
    """See exactly how DFS explores the decision tree"""
    all_subsets = []
    current_subset = []
    
    def dfs(index, depth=0):
        indent = "  " * depth
        print(f"{indent}DFS called: index={index}, current_subset={current_subset}")
        
        # BASE CASE
        if index == len(elements):
            print(f"{indent}→ BASE CASE: Saving {current_subset}")
            all_subsets.append(current_subset[:])
            return
        
        # RECURSIVE CASE
        element = elements[index]
        print(f"{indent}→ Deciding about element: {element}")
        
        # Choice 1: INCLUDE
        print(f"{indent}  Trying: INCLUDE {element}")
        current_subset.append(element)
        dfs(index + 1, depth + 1)
        current_subset.pop()
        print(f"{indent}  Back from INCLUDE {element}")
        
        # Choice 2: EXCLUDE
        print(f"{indent}  Trying: EXCLUDE {element}")
        dfs(index + 1, depth + 1)
        print(f"{indent}  Back from EXCLUDE {element}")
    
    dfs(0)
    return all_subsets

print("\n" + "="*50)
print("DETAILED DFS TRACE FOR [1, 2]:")
print("="*50)
traced_subsets = dfs_with_trace([1, 2])
print(f"\nFinal result: {traced_subsets}")

# ===================================
# THE DFS PATTERN YOU'LL USE EVERYWHERE
# ===================================

print("\n" + "="*60)
print("THE UNIVERSAL DFS PATTERN:")
print("="*60)
print("""
def dfs(current_state, remaining_decisions):
    # BASE CASE: No more decisions to make
    if no_more_decisions:
        process_complete_solution(current_state)
        return
    
    # RECURSIVE CASE: For each possible choice
    for choice in get_possible_choices():
        # 1. MAKE the choice
        make_choice(current_state, choice)
        
        # 2. GO DEEPER (this is the "Depth-First" part)
        dfs(modified_state, remaining_decisions)
        
        # 3. UNDO the choice (backtrack)
        undo_choice(current_state, choice)
""")

# ===================================
# KEY DFS CONCEPTS
# ===================================

print("\n" + "="*40)
print("KEY DFS CONCEPTS:")
print("="*40)
print("1. 🌳 DECISION TREE: Each level = one decision")
print("2. 📍 CURRENT STATE: Where we are right now")  
print("3. 🎯 BASE CASE: When we've made all decisions")
print("4. 🔄 RECURSION: Go deeper into the tree")
print("5. ↩️  BACKTRACK: Undo choice and try next option")
print("6. 🗂️  COLLECTION: Save solutions when we find them")

print("\n" + "="*40)
print("WHY DFS WORKS FOR SUBSETS:")
print("="*40)
print("• Each level asks: 'Include element X or not?'")
print("• We go deep (make all decisions) before trying alternatives")
print("• Backtracking lets us explore all possibilities")
print("• We naturally generate all 2^n subsets")

print("\n" + "="*40)
print("DFS vs LOOPS - MINDSET SHIFT:")
print("="*40)
print("❌ Loop thinking: 'Go through each element'")
print("✅ DFS thinking: 'For each element, try both choices (include/exclude)'")
print("❌ Loop: Linear progression")  
print("✅ DFS: Tree exploration with backtracking")