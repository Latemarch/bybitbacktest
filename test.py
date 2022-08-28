'''
import numpy as np  
a = [[1,2],[3,4],[5,4],[3,2]]
b = []
b.append([1])
b[-1].append(10)
b.append([2])
print(b)
b[-1].append(10)
print(b)

for i,val in enumerate(a): print(i,val)
'''
asset = [1,2,3]
position = 0
PL = 0
price = 1000
balance = [[0,0,100],[0,0,100]]
print(balance)
def buy(qty, position,asset):
    global PL
    print(qty,asset,PL)
    i = 0 if position == 'long' else 1
    balance[i][1] = price 
    asset.append(1)
buy(10,'long',asset)
print(balance)

