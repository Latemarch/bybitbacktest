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
history = [[[0,0]],[[0,0]],[[0,0]],[[0,0]],[0]]
#history[1].append([2])
#history[1][-1].append(2)
candletime = 1010
price = 4000
print(history)
print('---------')
def record_history(position,buyorsell):
    i = 1 if position == 'long' else 0
    k = 0 if buyorsell == 'buy' else 2
    history[i+k].append([candletime])
    history[i+k][-1].append(4000)
record_history('long','buy')
record_history('long','sell')
record_history('short','buy')
record_history('short','sell')
candletime = 2020
price = 8000
record_history('long','buy')
record_history('long','sell')
record_history('short','buy')
record_history('short','sell')
for i in range(4): 
    history[i].pop(0)
print(history[1])
history[4].append(1212)
for i, val in enumerate(history):
    print(val)
print(history[4][1])
