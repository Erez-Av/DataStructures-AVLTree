from AVLTree import AVLTree

T = AVLTree(True)

def printall():
    ls = T.avl_to_list()
    # print(ls)
    for i in ls:
        node = T.search(i[0])[0]
        print(f"key: {node.key}, succ: {node.successor.key}, pred: {node.predecessor.key}")
# printall()
# T.insert(5, "5")
def build(ls):
    for i in ls:
        T.insert(i,i)

ls = [25,19,7,22,30,16,13,50,66,56,1,10,75,59, 17, 2,52, 40,90,62, 68, 72, 14,18,11,3,9,8,73]#,100,70]
build(ls)

print(T)
# printall()
print()
node = T.search(66)[0]
T.delete(node)
print(T)
# node = T.search(11)[0]
# T.delete(node)
# node = T.search(8)[0]
# T.delete(node)
# node = T.search(66)[0]
# T.delete(node)
print()
# print(T)
# print(T.num_children(node),T.get_childeren(node))
# # node2 = T.search(6)[0]
# printall()

# print(T.get_childeren(node))
# print(T.get_height())
# print(T.root.left is T.root.right)
# print(T.root.left.key, T.root.right.right.parent.key )

