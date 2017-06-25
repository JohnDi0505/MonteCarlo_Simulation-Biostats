original_df <- read.csv("iris.csv")
df <- original_df[, -1]

# features array x
inputs <- df[, 1:ncol(df)-1]
inputs <- data.matrix(inputs)
x <- cbind(inputs, matrix(1, nrow = nrow(inputs), ncol = 1))
# target array t
target <- df[, ncol(df)]
target <- matrix(target, nrow = 150, ncol = 1)
categories <- unique(target)
t <- matrix(0, nrow = nrow(x), ncol = length(unique(target)))
for (i in 1:3) {
  t[which(target == categories[i]), i] <- 1
}
# construct target array to compare with output for computing accuracy
for (species.ix in 1:length(categories)) {
  ix <- which(target == categories[species.ix])
  target[ix,] <- species.ix
}
target <- as.numeric(target)

# create empty collection to store historical output
weights_collection <- list()
for (neuron in 1:ncol(t)){
  weights_collection[[neuron]] <- list()
  for (weight in 1: ncol(inputs)) {
    weights_collection[[neuron]][[weight]] <- list()
  }
}
accuracy <- list()

# initialize random weights (neuron=3, weights = 4 * 3)
eta <- 0.1
w <- matrix(runif(12, min = 1e-3, max = 1e-2), nrow = 4, ncol = 3)
b <- matrix(runif(3), nrow = 1, ncol = 3)
weights_biases <- rbind(w, b)

for (i in 1:1000) {
  # compute weighted linear combination
  weight_linear <- x %*% weights_biases
  # compute neuron activity y
  y <- exp(weight_linear) / rowSums(exp(weight_linear))
  # compute errors e <- t - y
  e <- t - y
  
  # update biases w_previous <- w_current - eta * (-sum(t - y) * x)
  weights_biases[nrow(weights_biases),] <- weights_biases[nrow(weights_biases), ] - eta * (-colSums(e)) / nrow(t)
  for (neuron in 1: ncol(t)) {
    # append weights
    for (weight in 1: ncol(inputs)) {
      weights_collection[[neuron]][[weight]][[i]] <- weights_biases[1:nrow(weights_biases) - 1, neuron][weight]
    }
    # update weights
    weights_biases[1:nrow(weights_biases) - 1, neuron] <- weights_biases[1:nrow(weights_biases) - 1, neuron] - eta * (-colSums(x[, 1:ncol(x) - 1] * e[, neuron])) / nrow(t)
  }
  
  # compute accuracy
  acc <- length(which(max.col(y) == target)) / nrow(t)
  accuracy <- append(accuracy, acc)
}

# visualize weights
cl <- rainbow(ncol(t))
plot(0, 0, xlim = c(1, 1000), ylim = c(-3, 3))
for (neuron in 1:ncol(t)) {
  for (weight in 1:ncol(inputs)) {
    lines(x = 1:1000, y = weights_collection[[neuron]][[weight]], col = cl[neuron], lty = weight)
  }
}
title("Weights Variation")

# visualize accuracy
plot(1:1000, accuracy)
title("accuracy")
