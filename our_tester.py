from AVLTree import AVLTree

T = AVLTree(True)

T.insert(10, "10")
T.insert(5, "5")
T.insert(15, "15")
T.insert(5, "20")
T.insert(22, "20")
T.insert(30, "30")
T.insert(6, "6")

print(T)
print(T.get_height())
# print(T.root.left is T.root.right)
# print(T.root.left.key, T.root.right.right.parent.key )
ls = T.avl_to_list()
print(ls)
for i in ls:
    node = T.search(i[0])[0]
    print(f"key: {node.key}, succ: {T.find_succ(node).key}, pred: {T.find_pred(node).key}")
    print(f"key: {node.key}, succ: {node.successor.key}, pred: {node.predecessor.key}")
