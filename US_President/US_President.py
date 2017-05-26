import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
 
df = pd.read_table("presidents.txt", names=["num", "name", "presidency"])
 
name_list = list(df.name)
 
# create a list to store matches after each shuffle
shuffle_record = []
 
# create a function in which the first argument is the original dataset; second argument is number of shuffles
def shuffler2(original, n):
    record = []
    for i in range(n):
        num = 0
        each_shuffle = {}
        temp = original.reindex(np.random.permutation(original.index)) # do shuffling for each
        compare = original.num == temp.num
        matched_df = original.ix[compare[compare == True].index]
        for i in matched_df.index:
            each_shuffle[i] = matched_df.name[i]
        shuffle_record.append(each_shuffle)
        try:
            num = compare.value_counts()[1]
        except:
            pass
        record.append(num)
    return(record)
result2 = shuffler2(df, 1000)
 
plt.hist(result2, color="yellow")
plt.title("Histgram for President Data")
plt.show()
