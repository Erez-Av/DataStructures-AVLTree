from AVLTree import AVLTree
import random
import time
import matplotlib.pyplot as plt

def exp_1(n):
    bst = AVLTree(False)
    total_operations = 0
    total_rotations = 0
    total_height_changes = 0
    start_time = time.time()
    
    for i in range(1, n+1):
        _, search_time, rotations, height_changes = bst.insert(i, str(i))
        total_operations += search_time + rotations + height_changes
        total_rotations += rotations
        total_height_changes += height_changes
        
    end_time = time.time()
    runtime_ms = (end_time - start_time) * 1000
    
    return bst.size(), bst.get_height(), total_rotations, total_height_changes, total_operations, runtime_ms

def exp_2(n):
    avl = AVLTree(True)
    total_operations = 0
    total_rotations = 0
    total_height_changes = 0
    start_time = time.time()
    
    for i in range(1, n+1):
        _, search_time, rotations, height_changes = avl.insert(i, str(i))
        total_operations += search_time + rotations + height_changes
        total_rotations += rotations
        total_height_changes += height_changes
        
    end_time = time.time()
    runtime_ms = (end_time - start_time) * 1000
    
    return avl.size(), avl.get_height(), total_rotations, total_height_changes, total_operations, runtime_ms

def exp_3(n):
    total_size = 0
    total_height = 0
    sum_rotations = 0
    sum_height_changes = 0
    sum_operations = 0
    sum_runtime_ms = 0

    numbers = [i for i in range(1, n+1)]
    
    for _ in range(20):
        bst = AVLTree(False)
        random.shuffle(numbers)
        
        operations_in_run = 0
        rotations_in_run = 0
        height_changes_in_run = 0
        start_time = time.time()

        for i in numbers:
            _, search_time, rotations, height_changes = bst.insert(i, str(i))
            operations_in_run += search_time + rotations + height_changes
            rotations_in_run += rotations
            height_changes_in_run += height_changes
            
        end_time = time.time()
        runtime_ms = (end_time - start_time) * 1000
        
        # צבירת הנתונים של ההרצה הנוכחית
        total_size += bst.size()
        total_height += bst.get_height()
        sum_rotations += rotations_in_run
        sum_height_changes += height_changes_in_run
        sum_operations += operations_in_run
        sum_runtime_ms += runtime_ms
        
    # החזרת הממוצע של כל מדד
    return (total_size / 20, 
            total_height / 20, 
            sum_rotations / 20, 
            sum_height_changes / 20, 
            sum_operations / 20, 
            sum_runtime_ms / 20)

def exp_4(n):
    total_size = 0
    total_height = 0
    sum_rotations = 0
    sum_height_changes = 0
    sum_operations = 0
    sum_runtime_ms = 0

    numbers = [i for i in range(1, n+1)]
    
    for _ in range(20):
        avl = AVLTree(True)
        random.shuffle(numbers)
        
        operations_in_run = 0
        rotations_in_run = 0
        height_changes_in_run = 0
        start_time = time.time()

        for i in numbers:
            _, search_time, rotations, height_changes = avl.insert(i, str(i))
            operations_in_run += search_time + rotations + height_changes
            rotations_in_run += rotations
            height_changes_in_run += height_changes
            
        end_time = time.time()
        runtime_ms = (end_time - start_time) * 1000
        
        # צבירת הנתונים של ההרצה הנוכחית
        total_size += avl.size()
        total_height += avl.get_height()
        sum_rotations += rotations_in_run
        sum_height_changes += height_changes_in_run
        sum_operations += operations_in_run
        sum_runtime_ms += runtime_ms
        
    # החזרת הממוצע של כל מדד
    return (total_size / 20, 
            total_height / 20, 
            sum_rotations / 20, 
            sum_height_changes / 20, 
            sum_operations / 20, 
            sum_runtime_ms / 20)

def get_perfect_tree_level_order(n):
    """בונה סדר הכנסה לפי רמות (BFS) כך שהעץ נבנה מושלם ללא אף רוטציה"""
    seq = []
    queue = [(1, n)]
    while queue:
        start, end = queue.pop(0)
        if start <= end:
            mid = (start + end) // 2
            seq.append(mid)
            queue.append((start, mid - 1))
            queue.append((mid + 1, end))
    return seq

def exp_5(n):
    avl = AVLTree(True)
    seq = get_perfect_tree_level_order(n)
    
    # 1. בניית העץ המושלם
    for i in seq:
        avl.insert(i, str(i))
        
    total_operations = 0
    total_rotations = 0
    total_height_changes = 0
    start_time = time.time()
    
    target_val = n + 1
    # 2. ביצוע הכנסה ומחיקה לסירוגין - רק על זה מודדים את הזמן והפעולות
    for _ in range(n):
        # מכניסים עלה חדש ומודדים
        _, search_time, rot, hc = avl.insert(target_val, str(target_val))
        total_operations += search_time + rot + hc
        total_rotations += rot
        total_height_changes += hc
        
        # מוחקים אותו כדי לשחזר את הרגישות של העץ
        node_to_delete, _ = avl.search(target_val)
        avl.delete(node_to_delete)
        
    end_time = time.time()
    runtime_ms = (end_time - start_time) * 1000
    
    # הוכחת המחץ לשאלה 5: פעולות האיזון (גלגולים + שינויי גובה) חלקי מספר ההכנסות
    amortized_balancing = (total_rotations + total_height_changes) / n
    
    return avl.size(), avl.get_height(), total_rotations, total_height_changes, total_operations, runtime_ms, amortized_balancing

#----------------------------------------



def run_all_exp_1():
    n_values = []
    runtimes_ms = []
    
    print(f"{'Size':<10} | {'Height':<8} | {'Rotations':<10} | {'Height Chg':<10} | {'Operations':<12} | {'Runtime (ms)':<15}")
    print("-" * 75)
    
    for i in range(1, 11):
        n = 300 * (2 ** i)
        n_values.append(n)
        
        size, height, rotations, height_changes, total_ops, runtime_ms = exp_1(n)
        runtimes_ms.append(runtime_ms)
        
        print(f"{size:<10} | {height:<8} | {rotations:<10} | {height_changes:<10} | {total_ops:<12} | {runtime_ms:<15.2f}")
        
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, runtimes_ms, marker='o', linestyle='-', color='blue')
    plt.title("Experiment 1: BST Sorted Insertion")
    plt.xlabel("n (Number of elements)")
    plt.ylabel("Runtime (ms)")
    plt.grid(True)
    plt.show()


def run_all_exp_2():
    n_values = []
    runtimes_ms = []
    
    print(f"{'Size':<10} | {'Height':<8} | {'Rotations':<10} | {'Height Chg':<10} | {'Operations':<12} | {'Runtime (ms)':<15}")
    print("-" * 75)
    
    for i in range(1, 11):
        n = 300 * (2 ** i)
        n_values.append(n)
        
        size, height, rotations, height_changes, total_ops, runtime_ms = exp_2(n)
        runtimes_ms.append(runtime_ms)
        
        print(f"{size:<10} | {height:<8} | {rotations:<10} | {height_changes:<10} | {total_ops:<12} | {runtime_ms:<15.2f}")
        
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, runtimes_ms, marker='o', linestyle='-', color='blue')
    plt.title("Experiment 2: AVL Sorted Insertion")
    plt.xlabel("n (Number of elements)")
    plt.ylabel("Runtime (ms)")
    plt.grid(True)
    plt.show()



def run_all_exp_3():
    n_values = []
    runtimes_ms = []
    
    print(f"{'Size':<10} | {'Height':<8} | {'Rotations':<10} | {'Height Chg':<10} | {'Operations':<12} | {'Runtime (ms)':<15}")
    print("-" * 75)
    
    for i in range(1, 11):
        n = 300 * (2 ** i)
        n_values.append(n)
        
        size, height, rotations, height_changes, total_ops, runtime_ms = exp_3(n)
        runtimes_ms.append(runtime_ms)
        
        print(f"{size:<10.0f} | {height:<8.2f} | {rotations:<10.2f} | {height_changes:<10.2f} | {total_ops:<12.2f} | {runtime_ms:<15.2f}")
        
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, runtimes_ms, marker='o', linestyle='-', color='blue')
    plt.title("Experiment 3: BST Random Insertion") 
    plt.xlabel("n (Number of elements)")
    plt.ylabel("Runtime (ms)")
    plt.grid(True)
    plt.show()




def run_all_exp_4():
    n_values = []
    runtimes_ms = []
    
    print(f"{'Size':<10} | {'Height':<8} | {'Rotations':<10} | {'Height Chg':<10} | {'Operations':<12} | {'Runtime (ms)':<15}")
    print("-" * 75)
    
    for i in range(1, 11):
        n = 300 * (2 ** i)
        n_values.append(n)
        
        size, height, rotations, height_changes, total_ops, runtime_ms = exp_4(n)
        runtimes_ms.append(runtime_ms)
        
        print(f"{size:<10.0f} | {height:<8.2f} | {rotations:<10.2f} | {height_changes:<10.2f} | {total_ops:<12.2f} | {runtime_ms:<15.2f}")
        
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, runtimes_ms, marker='o', linestyle='-', color='blue')
    plt.title("Experiment 4: AVL Random Insertion") 
    plt.xlabel("n (Number of elements)")
    plt.ylabel("Runtime (ms)")
    plt.grid(True)
    plt.show()

"""

def run_all_exp_5():
    n_values = []
    amortized_costs = []
    
    # הטבלה בדיוק בפורמט שרצית + עמודת ההוכחה
    print(f"{'Size':<10} | {'Height':<8} | {'Rotations':<10} | {'Height Chg':<10} | {'Operations':<12} | {'Runtime (ms)':<15} | {'Avg Bal. Ops / Insert'}")
    print("-" * 98)
    
    for i in range(1, 11):
        # מתאימים את הגודל לעצים מושלמים בגבהים עולים (מגובה 10 עד 19)
        h = i + 9
        n = (2 ** h) - 1
        n_values.append(n)
        
        size, height, rotations, height_changes, total_ops, runtime_ms, amortized = exp_5(n)
        amortized_costs.append(amortized)
        
        print(f"{size:<10} | {height:<8} | {rotations:<10} | {height_changes:<10} | {total_ops:<12} | {runtime_ms:<15.2f} | {amortized:<15.2f}")
        
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, amortized_costs, marker='o', linestyle='-', color='red')
    plt.title("Experiment 5: Proof of Non-Constant Amortized Balancing Cost")
    plt.xlabel("n (Number of elements)")
    plt.ylabel("Average Balancing Ops per Insertion")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    run_all_exp_5()