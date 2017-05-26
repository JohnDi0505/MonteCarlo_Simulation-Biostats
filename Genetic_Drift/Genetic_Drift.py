#Python
import numpy as np
import sys
from random import sample
import matplotlib.pyplot as plt
 
def simulator(gametes_rate, next_individuals, generations):
    individuals = [1 for i in range(50)] + [0 for j in range(50)]
    frequency = []
    for generation in range(generations):
        gametes = []
        for individual in individuals:
            gametes += [individual for i in range(gametes_rate)]
        individuals = sample(gametes, next_individuals)
        frequency.append(np.count_nonzero(individuals) / len(individuals))
    return(frequency)
 
N_100 = simulator(100, 100, 1000)
N_1000 = simulator(100, 1000, 1000)
 
# Create plots with pre-defined labels.
# Alternatively,pass labels explicitly when calling `legend`.
fig, ax = plt.subplots()
ax.plot(N_100, 'r', label='N=100')
ax.plot(N_1000, 'b', label='N=1000')
 
# Add x, y labels and title
plt.ylim(-0.1, 1.1)
plt.xlabel("Generation")
plt.ylabel("Frequency")
plt.title("Wright-Fisher Model")
 
# Now add the legend with some customizations.
legend = ax.legend(loc='upper right', shadow=True)
 
# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
frame = legend.get_frame()
frame.set_facecolor('0.90')
 
# Set the fontsize
for label in legend.get_texts():
    label.set_fontsize('large')
 
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.show()
