import numpy as np
import random



%%time
tsize=1000
result=[]

for i in range(tsize):
    result.append(0.23*np.sin(2*np.pi*i)+random.random())
    # print(0.23*np.sin(2*np.pi*i) + random.random())
  