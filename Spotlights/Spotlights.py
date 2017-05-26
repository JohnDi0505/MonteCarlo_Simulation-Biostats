import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
from random import sample
from itertools import combinations, permutations
from numpy import count_nonzero, array
 
def red_light(av, st):
    traffic_light = ["red_st", "red_av"]
    total_cross = av + st - 1
    while av != 0 and st != 0:
        if sample(traffic_light, 1)[0] == "red_st":
            av -= 1
        else:
            st -= 1
    rest_cross = av if av != 0 else st
    return(count_nonzero([sample([0, 1], 1) for corss in range(rest_cross)]))
 
df = DataFrame(0, index=np.arange(10), columns=np.arange(10))
 
simulation = 1000
for av in df.index:
    for st in df.index:
        df.loc[av, st] = sum(array([[red_light(av, st)] for n in range(simulation)])) / simulation
 
plt.imshow(df, cmap='hot', interpolation='nearest')
plt.xticks(np.arange(1, 10))
plt.yticks(np.arange(1, 10))
plt.title("Average Numbers Waiting for Red Light")
plt.xlabel("Number of Av")
plt.ylabel("Number of St")
plt.show()
 
 
# Recursive Function for Each Trial
 
from sys import stdout
av = 30
st = 30
n_space = [0]
traffic_light = ["red_st", "red_av"]
def route(av, st):
    if not av == st == 0:
        if sample(traffic_light, 1)[0] == "red_st":
            if av == 0:
                stdout.write("w_")
                n_space[0] += 1
                route(av, st - 1)
            else:
                stdout.write("\n" + " " * n_space[0] + "|")
                route(av - 1, st)
        else:
            if st == 0:
                stdout.write("\n" + " " * n_space[0] + "w" + "\n" + " " * n_space[0] + "|")
                route(av - 1, st)
            else:
                stdout.write("_")
                n_space[0] += 1
                route(av, st - 1)
route(av, st)
