import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import exp
from numpy.random import uniform

df = pd.read_csv("iris.csv")

# data pre-processing
df = df.drop([df.columns[0]], axis=1)
df = df.drop([df.columns[1], df.columns[3]], axis=1)
df = df[df["Species"] != "setosa"]
df.ix[df.Species == "versicolor", "Species"] = 1 # versicolor = 1
df.ix[df.Species == "virginica", "Species"] = 0 # virginica = 0
df = df.reset_index(drop=True)

# create collections to store historical weights & errors
weight1 = []
weight2 = []
bias = []
accuracy = []

def single_neuron_classifier(learning_rate, conf, generations):
    # claim training dataset & parameters
    x1 = np.array(df[df.columns[0]]) # sepal length
    x2 = np.array(df[df.columns[1]]) # petal length
    t = np.array(df[df.columns[2]]) # target
    eta = learning_rate
    inconf = 1 - conf
    
    # initialize random weigts: w1 & w2; initialize random bias
    weights = uniform(low=1e-3, high=1e-2, size=2)
    w1 = weights[0]
    w2 = weights[1]
    b = uniform(size=1)[0]
    
    weight1.append(w1) # insert initial weight1
    weight2.append(w2) # insert initial weight2
    bias.append(b) # insert initial bias
    
    # learning process
    for i in range(generations):
        # neuron activation
        a = w1 * x1 + w2 * x2
        # neuron activity/output
        y = 1 / (1 + exp(-a-b))
        # calculate error
        err = t - y
        # calculate accuracy based on a specified confidence
        acc = len(np.where((np.absolute(err) < inconf) == True)[0]) / len(t)
        accuracy.append(acc)
        # update weights & bias
        w1 = w1 - eta * ((-err * x1).sum()) # gradient_x1 = -err * x1
        weight1.append(w1)
        w2 = w2 - eta * ((-err * x2).sum()) # gradient_x2 = -err * x2
        weight2.append(w2)
        b = b - eta * (-err.sum()) # gradient_b = -err
        bias.append(b)

# function to plot the variation of accuracy overtime
def accuracy_variation():
    accur, = plt.plot(accuracy, label="Accuracy", color="black", linestyle="-", linewidth=2)
    
    plt.legend([accur], loc=2)
    plt.xlim([-5, 1000])
    plt.ylim([0, 1])
    plt.title("Accuracy Variation")
    plt.xlabel("Generation(t from 1 to 1000)")
    plt.ylabel("Accuracy")
    plt.show()
    
# function to plot weights variation
def weights_variation():
    w1, = plt.plot(weight1, label="Weight1 for Sepal Length", color="orange", linestyle="-", linewidth=3)
    w2, = plt.plot(weight2, label="Weight2 for Pepal Length", color="purple", linestyle="-", linewidth=3)
    
    plt.legend([w1, w2], loc=3)
    plt.title("Weights Variation")
    plt.xlabel("Generation(t from 1 to 1000)")
    plt.ylabel("Weights")
    plt.show()

# function to plot scatter plot & lines to seperate species
def classification_line():
    versicolor, = plt.plot(df[df["Species"] == 1]['Sepal.Length'], df[df["Species"] == 1]['Petal.Length'],
                           "bo",
                           label="versicolor",
                           markeredgewidth=3,
                           markersize=15)
    virginica, = plt.plot(df[df["Species"] == 0]['Sepal.Length'], df[df["Species"] == 0]['Petal.Length'],
                          "ro",
                          label="virginica",
                          markeredgewidth=3,
                          markersize=15)

    # classification line iteration=1000
    k = - weight1[-1] / weight2[-1]
    b = - bias[-1] / weight2[-1]
    x = np.random.randint(0, 15, 10)
    y = k * x + b
    line1000, = plt.plot(x, y, label="t=1000", color='k', linestyle='-', linewidth=3)
    # classification line iteration=100
    k100 = - weight1[100] / weight2[100]
    b100 = - bias[100] / weight2[100]
    y100 = k100 * x + b100
    line100, = plt.plot(x, y100, label="t=100", color='g', linestyle='--', linewidth=3)
    # classification line iteration=50
    k50 = - weight1[50] / weight2[50]
    b50 = - bias[50] / weight2[50]
    y50 = k50 * x + b50
    line50, = plt.plot(x, y50, label="t=50", color='y', linestyle='--', linewidth=3)
    
    # plot legend
    plt.legend([versicolor, virginica, line1000, line100, line50], loc=4)
    
    plt.xlim([df[df.columns[0]].min() - 0.5, df[df.columns[0]].max() + 0.5])
    plt.ylim([df[df.columns[1]].min() - 0.5, df[df.columns[1]].max() + 0.5])
    plt.title("Species Seperation Lines")
    plt.xlabel("Sepal Length")
    plt.ylabel("Petal Length")
    plt.show()
    
# run this python script
if __name__ == "__main__":
    single_neuron_classifier(0.1, 0.95, 1000)
    accuracy_variation()
    weights_variation()
    classification_line()
