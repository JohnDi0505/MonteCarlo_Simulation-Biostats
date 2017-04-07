import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from random import sample
from numpy.random import choice
from numpy.random import poisson
from operator import itemgetter

# global variables
nuc = np.array(["A", "T", "C", "G"])
expected_mutation_rate = 0.00001 # there are 2 sequences per individual
seq_length = 10000
individual_pop = 100
gamete_rate = 100
generation = 1000

def simulator(population, repro_rate, generation):
    observed_mutation_collection = []
    
    # Original Individuals
    original = choice(nuc, seq_length, 0.25)
    individual_total = [original for i in range(population)]
    
    for i in range(generation): # iterate over 1000 generations
        # Produce Gametes
        gametes = []
        for individual in individual_total:
            gametes += [individual for i in range(repro_rate)]
        gametes = np.array(gametes)
        gametes_pop = gametes.shape[0] # number of gametes: 100 * 100
        
        # Mutation
        mutation_number_arr = poisson(lam=seq_length * expected_mutation_rate, size=gametes_pop) # derive number of mutations per individual
        mutation_index_arr = [sample(range(seq_length), mutations) for mutations in mutation_number_arr] # get the index of mutation
        # Mutation: Replace with Mututated Base Pairs
        for i in range(gametes_pop): # iterate over all gametes
            for ix in mutation_index_arr[i]: # iterate over mutated base pair for each gamete
                gametes[i, ix] = choice(nuc[nuc != gametes[i, ix]], 1)[0] # locate mutation and alter the nuc with mutated one
        
        # Next generation of individuals
        individual_total = gametes[choice(range(10000), 100, replace=False)]
        
        # Calculate observed mutation rate
        num_combinations = 0
        total_diff_bases = 0
        for pair in combinations(range(len(individual_total)), 2): # aggregate mutations for all possible pairs of individuals
            total_diff_bases += len(np.where((individual_total[pair[0]] == individual_total[pair[1]]) == False)[0])
            num_combinations += 1
        observed_mutation_rate = float(total_diff_bases) / float(num_combinations) / seq_length
        observed_mutation_collection.append(observed_mutation_rate)
        
    return(observed_mutation_collection)

# Running simulation
result = simulator(100, 100, 1000)

# Visualizing results
plt.plot(result, 'b')
plt.xlabel("Generation")
plt.ylabel("Mutation Rate")
plt.title("Drift-Mutation Balance")
plt.show()
