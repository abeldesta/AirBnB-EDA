import pandas as pd 
import numpy as np 
import scipy.stats as stats
import random 
import matplotlib.pyplot as plt 
plt.style.use('ggplot')

#read in datasets
nyc = pd.read_csv('data/nyc_data.csv')
madrid = pd.read_csv('data/madrid_data.csv')

#Sampling Class to sample data to find distributes of an attribute
class Sampling(object):
    def __init__(self, data, column_name):
        self.data = data
        self.test_col = column_name

    def sample_repeated_sum(self, n_samples, n_summands):
        """Sample n_samples from the sum of n_summands iid copies of a random
        varaible.
        """
        samples = np.array(random.choices(self.data[self.test_col], k = n_samples*n_summands)).reshape(n_samples, n_summands)
        return np.sum(samples, axis = 1)
    
    def sample_repeated_var(self, n_samples, n_summands):
        """Sample n_samples from the variance of n_summands iid copies of a random
        varaible.
        """
        samples = np.array(random.choices(self.data[self.test_col], k = n_samples*n_summands)).reshape(n_samples, n_summands)
        return np.var(samples, ddof = 1, axis = 1)

    def sample_means(self, n_samples, n_summands):
        return (1/n_summands) * (sample_repeated_sum(n_samples, n_summands))

    def CLT(self, n_samples, n_summands):
        return sample_means(n_samples, n_summands).mean()

    def bootstrap(self, n_samples, n_summands):
        return np.var(sample_repeated_var(n_samples, n_summands), ddof=1)


class HypoTest(object):
    def __init__(self, data, alpha):


if __name__ == "__main__":
    #NYC EDA
    print(nyc.info())
