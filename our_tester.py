from AVLTree import AVLTree

T = AVLTree(True)

def printall():
    ls = T.avl_to_list()
    # print(ls)
    for i in ls:
        node = T.search(i[0])[0]
        print(f"key: {node.key}, succ: {node.successor.key}, pred: {node.predecessor.key}")
# printall()
T.insert(10, "10")
# T.insert(5, "5")
T.insert(15, "15")
# T.insert(5, "20")
T.insert(22, "20")
T.insert(30, "30")
T.insert(31, "31")
# T.insert(32, "31")
# T.insert(33, "31")
T.insert(6, "6")
T.insert(11, "3")
# T.insert(9, "3")

print(T)
# printall()
# print()
# node = T.search(10)[0]
# # print(T.num_children(node),T.get_childeren(node))
# T.delete(node)
# # node2 = T.search(6)[0]
# print(T)
# printall()
# print()

# print(T.get_childeren(node))
# print(T.get_height())
# print(T.root.left is T.root.right)
# print(T.root.left.key, T.root.right.right.parent.key )

