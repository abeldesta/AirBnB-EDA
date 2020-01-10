import pandas as pd 
import numpy as np 
import scipy.stats as stats
from statsmodels.stats.weightstats import ztest
import random 
import matplotlib.pyplot as plt 
import geopandas 
import geoplot
plt.style.use('ggplot')

#Sampling Class to sample data to find distributes of an attribute
class Sampling(object):
    def __init__(self, data, column_name):
        self.data = data[column_name]
        self.test_col = column_name

    def sample_repeated_sum(self, n_samples, n_summands):
        """Sample n_samples from the sum of n_summands iid copies of a random
        varaible.
        """
        samples = np.array(random.choices(self.data, k = n_samples*n_summands)).reshape(n_samples, n_summands)
        return np.sum(samples, axis = 1)
    
    def sample_repeated_var(self, n_samples, n_summands):
        """Sample n_samples from the variance of n_summands iid copies of a random
        varaible.
        """
        samples = np.array(random.choices(self.data, k = n_samples*n_summands)).reshape(n_samples, n_summands)
        return np.var(samples, ddof = 1, axis = 1)

    def sample_means(self, n_samples, n_summands):
        return (1/n_summands) * (self.sample_repeated_sum(n_samples, n_summands))

    def CLT(self, n_samples, n_summands):
        return self.sample_means(n_samples, n_summands).mean()

    def bootstrap(self, n_samples, n_summands):
        bootstrap_samp = []
        for i in range(n_samples):
            bootstrap = np.random.choice(self.data, size= n_summands, replace=True)
            bootstrap_var = np.var(bootstrap)
            bootstrap_samp.append(bootstrap_var)
        return bootstrap_samp

class HypoTest(object):
    def __init__(self, data1, data2, test_col, alpha):
        self.sample1 = data1[test_col]
        self.sample2 = data2[test_col]
        self.alpha = alpha

    def test(self, value = 0, alternative = 'two-sided'):
        self.zscore, self.pval = ztest(self.sample1, self.sample2, value=value, alternative = alternative)
        if self.pval < self.alpha:
            self.result = 'Reject the Null Hypothesis'
        else:
            self.result = 'Fail to Reject the Null Hypothesis'
        return self.result
        

        

if __name__ == "__main__":
    nyc = pd.read_csv('data/nyc_data.csv')
    madrid = pd.read_csv('data/madrid_data.csv')

    manhattan = nyc[nyc['neighbourhood_group'] == 'Manhattan'].reset_index()
    not_manhattan = nyc[nyc['neighbourhood_group'] != 'Manhattan'].reset_index()
    man_vs_city = HypoTest(manhattan, not_manhattan, 'price', 0.05)



    print('''
    H0: Mean price of Manhattan and all other boroughs are equal
    Ha: Mean price of Manhattan is greater than mean price of all other boroughs 

    alpha = 0.05, p_value = {1} 
    
    Result: {0}'''.format(man_vs_city.test(0, 'larger'), man_vs_city.pval))

    print('''
    -----------------------''')

    mad_vs_nyc = HypoTest(nyc, madrid, 'price', 0.05)

    print('''
    H0: Mean price of NYC and Madrid are equal
    Ha: Mean price of NYC is greater than mean price of Madrid

    alpha = 0.05, p_value = {1} 
    
    Result: {0}'''.format(mad_vs_nyc.test(0, 'larger'), mad_vs_nyc.pval))

    print('''
    -----------------------''')

    man_vs_mad = HypoTest(manhattan, madrid, 'price', 0.05)

    print('''
    H0: Mean price of Manhattan and Madrid are equal
    Ha: Mean price of Manhattan is greater than mean price of Madrid

    alpha = 0.05, p_value = {1} 
    
    Result: {0}'''.format(man_vs_mad.test(0, 'larger'), man_vs_mad.pval))
    
    centro  = madrid[madrid['neighbourhood_group'] == 'Centro'] 

    print('''
    -----------------------''')

    man_vs_cent = HypoTest(manhattan, centro, 'price', 0.05)

    print('''
    H0: Mean price of Manhattan, NY and Centro, Madrid are equal.
    Ha: Mean price of Manhattan NY is greater than mean price of Centro, Madrid.

    alpha = 0.05, p_value = {1} 
    
    Result: {0}'''.format(man_vs_cent.test(0, 'larger'), man_vs_cent.pval))
    