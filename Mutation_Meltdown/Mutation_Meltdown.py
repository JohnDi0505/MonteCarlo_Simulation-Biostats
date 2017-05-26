import numpy as np
import matplotlib.pyplot as plt
from numpy.random import poisson
from numpy.random import choice
 
def simulator(seq_length, pop, repro_rate, generations):
    mutation_rate = 0.00001
    lam = seq_length * mutation_rate
    individuals = np.array([1 for i in range(pop)])
    non_mutated_pop_rate = []
    for generation in range(generations):
        gametes = []
        for individual in individuals:
            off_sprs = poisson(lam, repro_rate)
            mutation_ix = np.array(np.where(off_sprs != 0))
            indiv_gametes = np.array([individual for j in range(repro_rate)])
            indiv_gametes[mutation_ix] = 0
            gametes += list(indiv_gametes)
        individuals = choice(gametes, size=pop)
        non_mutated_frequency = float(np.count_nonzero(individuals)) / pop
        non_mutated_pop_rate.append(non_mutated_frequency)
    return non_mutated_pop_rate
 
genome_length_1000 = 1000
genome_length_10000 = 10000
results_1000 = simulator(genome_length_1000, 1000, 100, 500)
results_10000 = simulator(genome_length_10000, 1000, 100, 500)
 
genome_length_1000 = 1000
genome_length_10000 = 10000
results2_1000 = simulator(genome_length_1000, 10000, 100, 500)
results2_10000 = simulator(genome_length_10000, 10000, 100, 500)
 
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
line_1_1000 = ax1.plot(results_1000, "r")
line_1_10000 = ax1.plot(results_10000, "b")
line_2_1000 = ax2.plot(results2_1000, "r")
line_2_10000 = ax2.plot(results2_10000, "b")
 
ax1.set_title("Population = 1000")
ax2.set_title("Population = 10000")
 
plt.title("Mutation Meltdown")
plt.show()
