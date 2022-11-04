# print('Test')
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import multivariate_normal
from scipy.stats import norm
import statistics

# # A priori knowledge
m1 = np.array([0.4, 0.8]) # mean values for class ω_1
m2 = np.array([1.5, 2.7]) # mean values for class ω_2
cov_mat = np.array([[1.5, 0], [0, 0.8]]) # covariance matrix for the 2 data indicators
p_1 = 0.95 # a priori probability for class ω_1
p_2 = 0.05 # a priori probability for class ω_2


#Function that configures the typical numpy.linespace function so that we can define the step,
#instead of the numbers of samples (num)
def linspace(start, stop, step=1.):
  """
    Like np.linspace but uses step instead of num
    This is inclusive to stop, so if start=1, stop=3, step=0.5
    Output is: array([1., 1.5, 2., 2.5, 3.])
  """
  return np.linspace(start, stop, int((stop - start) / step + 1))


# # ***Task A.1***
# # Initializing the random seed
random_seed = 1000

#Gaussian distribution for ω1 class "healthy people"
distr1 = multivariate_normal(cov = cov_mat, mean = m1, seed = random_seed)
#Gaussian distribution for ω2 class "possible existence of cancer"
distr2 = multivariate_normal(cov = cov_mat, mean = m2, seed = random_seed)

#Setting as sigma_i the main diagonal values of the common covariance matrix
sigma1, sigma2 = cov_mat[0, 0], cov_mat[1, 1]

# We make the values of the x vector, where x = (x1, x2).
# We take x1 in a range where: 
#   minimum value = min_value(of the μ1 and μ2 first value) - 3*sigma1
#   maximum value = max_value(of the μ1 and μ2 first value) + 3*sigma1
# AS for the x2 on the other hand we take value in a range where:
#   minimum value = min_value(of the μ1 and μ2 second value) - 3*sigma2
#   maximum value = max_value(of the μ1 and μ2 second value) + 3*sigma2
# We followed this procedure based on the method as described on rederence[1]
x1 = linspace(m1[0] - 3*sigma1, m2[0] + 3*sigma1, step=0.1)
x2 = linspace(m1[1] - 3*sigma1, m2[1] + 3*sigma1, step=0.1)
X1, X2 = np.meshgrid(x1, x2)

#We form the pdf for the Gaussian distribution of the first class ω1
pdf1 = np.zeros(X1.shape)
for i in range(X1.shape[0]):
    for j in range(X1.shape[1]):
        pdf1[i, j] = distr1.pdf([X1[i, j], X2[i, j]])

#We form the pdf for the Gaussian distribution of the second class ω2
pdf2 = np.zeros(X1.shape)
for i in range(X1.shape[0]):
  for j in range(X1.shape[1]):
    pdf2[i, j] = distr2.pdf([X1[i, j], X2[i, j]])


#plotting in the same 3-D figure the two Probability Density Functions
fig = plt.figure(figsize=(15, 10))
ax = plt.axes(projection = '3d')
plt.title("p(x|ω1) and p(x|ω2) for descrete x values following a Gaussian Distribution with μ1=(0.4, 0.8), μ2=(1.5, 2.7) and Σ=([1.5, 0], [0, 0.8])")
plt.xlabel("x_a biological indicator")
plt.ylabel("x_b biological indicator")
ax.set_zlabel("pdf value")
ax.plot_surface(X1, X2, pdf1, color="green")
ax.plot_surface(X1, X2, pdf2, color="red")
plt.legend(loc="upper right")
# plt.show()

# # ***Task A.2***
# Total Probability: P(x) = p(x|ω1)*P(ω1) + p(x|ω2)*P(ω2)
p = pdf1 * p_1 + pdf2 * p_2

#Plotting the total PDF in a 3-D figure
fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection = '3d')
plt.title("Total Probability Distribution")
plt.xlabel("x_a biological indicator")
plt.ylabel("x_b biological indicator")
ax.set_zlabel("Value of total pdf")
ax.plot_surface(X1, X2, p)
# plt.show()


# Task A.3

#A posteriori probabilities according to Bayes Theorem:
# p(ω1|x) = (p(x|ω1)/P(x)) * P(ω1)
# p(ω2|x) = (p(x|ω2)/P(x)) * P(ω2)

p_aposteriori_1 = (pdf1/p) * p_1
p_aposteriori_2 = (pdf2/p) * p_2

#Plotting the two a-posteriori probabilites as calculated from the Bayes Theorem
fig = plt.figure(figsize=(10, 10)) # prepare a figure
ax = plt.axes(projection = '3d')
plt.title("A-posteriori probabilities P(ω1|x) and P(ω2|x) according to Bayes Theorem")
plt.xlabel("x_a indicator")
plt.ylabel("x_b indicator")
ax.set_zlabel("Value of both A-posteriori probabilities")
ax.plot_surface(X1, X2, p_aposteriori_1)
ax.plot_surface(X1, X2, p_aposteriori_2)
plt.show()


# Task A.4

# Bayesian error
errors = np.zeros(pdf1.shape);
for i in range(len(X1)):
    for j in range(len(X1[0])):
        if pdf1[i][j] > pdf2[i][j]:
            # true is class 1 and the error is to choose class 2
            errors[i][j] = pdf2[i][j] * p_2;
        elif pdf1[i][j] < pdf2[i][j]:
            # true is class 2 and the error is to choose class 1
            errors[i][j] = pdf1[i][j] * p_1;
        else:
            errors[i][j] = 0;

error_sum = sum(errors) # get the sum of each row
new_error_sum = sum(error_sum) # get the final sum
error_mean = new_error_sum/(len(errors)*len(errors[0]));
print("The mean bayesian error is:" + str(error_mean))
