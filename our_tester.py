from AVLTree import AVLTree
import time

T = AVLTree(True)
S = AVLTree(False)
def printall():
    ls = T.avl_to_list()
    # print(ls)
    for i in ls:
        node = T.search(i[0])[0]
        print(f"key: {node.key}, succ: {node.successor.key}, pred: {node.predecessor.key}")
# printall()
# T.insert(5, "5")
def build(tree,ls):
    for i in ls:
        tree.insert(i,i)

ls = [25,19,7,22,30,16,13,50,66,56,1,10,75,59, 17, 2,52, 40,90,62, 68, 72, 14,18,11,3,9,8,73]#,100,70]
build(T,ls)

print(T)
x = T.insert(63,51)
# printall()
print()
# # # printall()
# print()
print(T)
z=T.insert(510,51)
node = T.search(56)[0]
# print(node.height)
# print()
# print(T)
# print(z[0].key, z[1:])
# print(T.avl_to_list())
node = T.search(56)[0]
T.delete(node)
node = T.search(52)[0]
T.delete(node)
node = T.search(62)[0]
T.delete(node)
print(T)
# print()
# print(len(ls),T.size())

# n = 20
# print(ls[:n])
# build(S, ls[:n])
# print(S)
# node = T.search(11)[0]
# T.delete(node)
# node = T.search(8)[0]
# T.delete(node)
# node = T.search(66)[0]
# T.delete(node)
# print(T)
# print(T.num_children(node),T.get_childeren(node))
# # node2 = T.search(6)[0]
# printall()

# print(T.get_childeren(node))
# print(T.get_height())
# print(T.root.left is T.root.right)
# print(T.root.left.key, T.root.right.right.parent.key )

S = AVLTree(False)
n = 10
for i in range(n):
    S.insert(i,i)
# t0 = time.time()
# a = S.avl_to_list()
# t1 = time.time()

# print(t1-t0)
# print(S.root)
print("\n\n")
x=S.insert(n+1,n+1)
S.insert(-1,-1)
print(x)
print(S)
print(S.get_height())
S.delete(x[0])
print(S)
print(S.get_height())
# print(S.root.left.key,S.root.right.key)
# S.insert(2,2)
# node = S.search(2)[0]
# print(node.left.key,node.right.key)
# print(S.root.left.key,S.root.right.key)
