from Bio import Phylo
from io import StringIO
from random import sample
from scipy.misc import comb
from itertools import combinations
from numpy.random import exponential as exp

# Generate Random Tree with Nodes & Waiting Time
individuals = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
node_dict = {}
reference = {}
wait_time_ref = {}
node = 0
while len(individuals) != 1:
    node_dict[node] = {"child_nodes": []}
    sample_events = tuple(sample(individuals, 2))
    reference[sample_events] = node
    wait_time = exp(1/comb(len(individuals), 2))
    wait_time_ref[node] = wait_time
    for sample_event in sample_events:
        if type(sample_event) == str:
            node_dict[node]["child_nodes"].append(sample_event)
        else:
            child_node = reference[sample_event]
            node_dict[node]["child_nodes"].append(child_node)
    individuals.remove(sample_events[0])
    individuals.remove(sample_events[1])
    individuals.append(sample_events)
    node += 1
    
# Calculate Tree Branch Lengths
tree_dict = {}
cumulative_br_length = 0
cumulative_br_len_dict = {}
for i in range(len(node_dict)):
    tree_dict[i] = {}
    cumulative_br_length += wait_time_ref[i]
    cumulative_br_len_dict[i] = cumulative_br_length
    for node in node_dict[i]['child_nodes']:
        if type(node) == str:
            tree_dict[i][node] = cumulative_br_length
        else:
            tree_dict[i][node] = cumulative_br_len_dict[i] - cumulative_br_len_dict[node]
            
# Parse the Tree into String
for i in range(len(tree_dict)):
    for node in tree_dict[i].keys():
        if type(node) != str:
            temp = str(tree_dict[node])
            tree_dict[i][temp] = tree_dict[i].pop(node)
tree_str = str(tree_dict[i]).replace('\'', '').replace('\"', '').replace('\\', '').replace('{', '(').replace('}', ')')            

# Visualize Tree
handle = StringIO(tree_str)
tree = Phylo.read(tree_str, "newick")
tree.ladderize()   # Flip branches so deeper clades are displayed at top
Phylo.draw(tree)
