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

    def bootstrap(self, n_samples):
        bootstrap_samp = []
        for i in range(n_samples):
            bootstrap = np.random.choice(self.data, size=len(self.data), replace=True)
            bootstrap_var = np.var(bootstrap)
            bootstrap_samp.append(bootstrap_var)
        return bootstrap_samp


if __name__ == "__main__":
    #NYC EDA
    print(nyc.info())

    neighborhood_listing_count = nyc['neighbourhood'].value_counts()
    top20_nyc_neighborhoods = neighborhood_listing_count[:20]
    top20_labels = top20_nyc_neighborhoods.index

    type_listings_nyc = nyc.groupby(['room_type', 'neighbourhood']).agg({'room_type':'count'})
    top20_entire_home_count = [type_listings_nyc.loc[('Entire home/apt', i)]['room_type'] for i in top20_labels]
    top20_private_room_count = [type_listings_nyc.loc[('Private room', i)]['room_type'] for i in top20_labels]
    top20_shared_room_count = [type_listings_nyc.loc[('Shared room', i)]['room_type'] for i in top20_labels]

    ##Bar plot
    fig, ax = plt.subplots(1,1)
    width = 0.8
    tickLocals = np.arange(20)
    ax.barh(tickLocals, top20_nyc_neighborhoods[::-1], width)
    ax.set_yticks(ticks = tickLocals)
    ax.set_yticklabels(top20_labels[::-1])
    plt.tight_layout(pad=1)
    plt.savefig('images/top20_neighbourhood_nyc.png')

    ##Side by side bar chart 
    fig, ax = plt.subplots(1,1, figsize = (12, 6))
    width = 0.2
    tickLocals = np.arange(10)
    ax.bar(tickLocals-2*width, top20_entire_home_count[:10], width, color = 'red', label = 'Entire Home/Apt')
    ax.bar(tickLocals-width, top20_private_room_count[:10], width, color = 'blue', label = 'Private room')
    ax.bar(tickLocals, top20_shared_room_count[:10], width, color = 'green', label = 'Shared room')
    ax.set_xticks(ticks = tickLocals)
    ax.set_xticklabels(top20_labels[:10])
    plt.xticks(rotation = 80)
    plt.legend()
    plt.tight_layout(pad=1)
    plt.savefig('images/top20_room_type.png')
    
    samp = Sampling(data = nyc, column_name = 'price')
    random.seed(53194)
    boot_var = samp.bootstrap(20000)
    
    ##Bootstrap sample variance of NYC price
    fig, ax = plt.subplots(1, 1)
    ax.hist(boot_var, bins = 50)
    ax.set_title('Bootstrap Sample Variance in NYC Listing Price (20000 samples)')
    plt.savefig('images/bootstapVar_Hist.png')

    ##Sample distribution of the mean price in NYC
    means = samp.sample_means(20000, 1000)
    fig, ax = plt.subplots(1, 1)
    ax.hist(means, bins = 50)
    ax.set_title('Sample Means in NYC Listing Price (20000 samples)')
    plt.savefig('images/sample_means_hist.png')

    #Hypothesis Testing for Mean Price of sample vs population 


