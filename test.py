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
