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
    for i in range(1, n+1):
        avl.insert(i)

def exp_3(n):
    bst = AVLTree(False)
    numbers = [i for i in range(1, n+1)]
    random.shuffle(numbers)
    for i in numbers:
        bst.insert(i)

def exp_4(n):
    avl = AVLTree(True)
    numbers = [i for i in range(1, n+1)]
    random.shuffle(numbers)
    for i in numbers:
        avl.insert(i)

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

if __name__ == "__main__":
    run_all_exp_1()