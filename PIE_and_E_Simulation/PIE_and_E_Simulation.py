# Simulate pi
simulation = 10000
distances = np.array([pow(uniform(0, 1), 2) + pow(uniform(0, 1), 2) for i in range(simulation)])
pi = count_nonzero(distances < 1) / simulation * 4
pi
 
# Simulate e
total = 10000
ranges = [[x/total, (x+1)/total] for x in range(total)]
sample_space = [uniform(0, 1) for x in range(total)]
index = []
for i in range(total):
    if any(ranges[i][0] <= point <= ranges[i][1] for point in sample_space):
        index.append(i)
e = total / (total - len(set(index)))
e
