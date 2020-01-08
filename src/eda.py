import pandas as pd 
import numpy as np 
import scipy.stats as stats
import random 
import matplotlib.pyplot as plt 
import geopandas 
import geoplot
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

    def bootstrap(self, n_samples, n_summands):
        bootstrap_samp = []
        for i in range(n_samples):
            bootstrap = np.random.choice(self.data, size= n_summands, replace=True)
            bootstrap_var = np.var(bootstrap)
            bootstrap_samp.append(bootstrap_var)
        return bootstrap_samp

def top_20(data, col_name):
    count = data[col_name].value_counts()
    top20 = count[:20]
    labels = top20.index
    return labels, top20

def bar_plot(data, labels):
    fig, ax = plt.subplots(1,1)
    width = 0.8
    tickLocals = np.arange(len(data))
    ax.barh(tickLocals, data[::-1], width)
    ax.set_yticks(ticks = tickLocals)
    ax.set_yticklabels(labels[::-1])
    plt.tight_layout(pad=1)
    
def side_by_side_bar(data1, data2, data3, labels):
    fig, ax = plt.subplots(1,1, figsize = (12, 6))
    width = 0.2
    tickLocals = np.arange(len(data1))
    ax.bar(tickLocals-2*width, data1[:10], width, color = 'red', label = 'Entire Home/Apt')
    ax.bar(tickLocals-width, data2[:10], width, color = 'blue', label = 'Private room')
    ax.bar(tickLocals, data3[:10], width, color = 'green', label = 'Shared room')
    ax.set_xticks(ticks = tickLocals)
    ax.set_xticklabels(labels[:10])
    plt.xticks(rotation = 80)
    plt.legend()
    plt.tight_layout(pad=1)


def geo_df(df, x = 'longitude', y = 'latitude'):
    return geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df[x], df[y]))

def nested_dictionary(data, col_name):
    unique_vals = set(data[col_name])
    subdatasets = dict()
    for i in unique_vals:
        subdatasets[i] = geo_df(data[data[col_name] == i])
    return subdatasets

def geomap_plot(d, base_map, color_dict):
    fig, ax = plt.subplots(1,1)
    ax.set_aspect('equal')
    base = base_map.plot(ax = ax, alpha=0.5, edgecolor='k')
    for k,v in d.items():
        v.plot(ax = ax, marker='d', c=color_dict[k], markersize=3, label = k)
    plt.legend()

colors = ['dodgerblue', 'salmon', 'navajowhite', 'yellowgreen', 'mediumorchid', 'lawngreen', 'orange', 'forestgreen', 'darkmagenta',
          'crimson', 'darkgoldenrod', ' mediumpurple', 'aqua', 'lightcoral', "violet", 'red', 'greeen', 'teal', 'hotpink', 'silver', 'black', 'gold']

def color_dict(lst, df, col_name):
    vals = set(df[col_name])
    subset = random.sample(lst, k = len(vals))
    col_dict = {k: subset[idx] for idx, k in enumerate(vals)}
    return col_dict



if __name__ == "__main__":
    #NYC EDA
    print(nyc.info())
    print(nyc.describe())

    ##NYC EDA

    neighborhood_listing_count = nyc['neighbourhood'].value_counts()
    top20_nyc_neighborhoods = neighborhood_listing_count[:20]
    top20_labels = top20_nyc_neighborhoods.index

    type_listings_nyc = nyc.groupby(['room_type', 'neighbourhood']).agg({'room_type':'count'})
    top20_entire_home_count = [type_listings_nyc.loc[('Entire home/apt', i)]['room_type'] for i in top20_labels]
    top20_private_room_count = [type_listings_nyc.loc[('Private room', i)]['room_type'] for i in top20_labels]
    top20_shared_room_count = [type_listings_nyc.loc[('Shared room', i)]['room_type'] for i in top20_labels]

    ##MADRID EDA
    neighborhood_listing_count_madrid = madrid['neighbourhood'].value_counts()
    top20_madrid_neighborhoods = neighborhood_listing_count[:20]
    top20_labels_madrid = top20_nyc_neighborhoods.index

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
    boot_var = samp.bootstrap(20000, 1000)
    
    # ##Bootstrap sample variance of NYC price
    # fig, ax = plt.subplots(1, 1)
    # ax.hist(boot_var, bins = 50)
    # ax.set_title('Bootstrap Sample Variance in NYC Listing Price')
    # plt.savefig('images/bootstapVar_Hist.png')

    # ##Sample distribution of the mean price in NYC
    # means = samp.sample_means(20000, 1000)
    # fig, ax = plt.subplots(1, 1)
    # ax.hist(means, bins = 50)
    # ax.set_title('Sample Means in NYC Listing Price')
    # plt.savefig('images/sample_means_hist.png')

    
    #Create a map of New York with the listings plotted
    nyc_map = geopandas.read_file('borough/geo_export_91122496-4899-4211-a64b-3cf55c0ddeae.shp')
    bk = nyc[nyc['neighbourhood_group'] == 'Brooklyn']
    hat = nyc[nyc['neighbourhood_group'] == 'Manhattan']
    queen = nyc[nyc['neighbourhood_group'] == 'Queens']
    staten = nyc[nyc['neighbourhood_group'] == 'Staten Island']
    bronx = nyc[nyc['neighbourhood_group'] == 'Bronx']
    gbk = geopandas.GeoDataFrame(bk, geometry=geopandas.points_from_xy(bk.longitude, bk.latitude))
    ghat = geopandas.GeoDataFrame(hat, geometry=geopandas.points_from_xy(hat.longitude, hat.latitude))
    gq = geopandas.GeoDataFrame(queen, geometry=geopandas.points_from_xy(queen.longitude, queen.latitude))
    gstat = geopandas.GeoDataFrame(staten, geometry=geopandas.points_from_xy(staten.longitude, staten.latitude))
    gbron = geopandas.GeoDataFrame(bronx, geometry=geopandas.points_from_xy(bronx.longitude, bronx.latitude))


    fig, ax = plt.subplots(1,1, figsize = (12,12))
    ax.set_aspect('equal')
    #colors = {'Brooklyn': 'dodgerblue', 'Bronx': 'salmon', 'Manhattan': 'navajowhite', 'Staten Island': 'yellowgreen', 'Queens': 'mediumorchid'}
    base = nyc_map.plot(ax = ax, alpha=0.5, edgecolor='k')
    gbk.plot(ax = ax, marker='d', color='dodgerblue', markersize=3, label = 'Brooklyn')
    ghat.plot(ax = ax, marker='.', color='navajowhite', markersize=3, label = 'Manhattan')
    gstat.plot(ax = ax, marker='p', color='yellowgreen', markersize=3, label = 'Staten Island')
    gq.plot(ax = ax, marker='*', color='mediumorchid', markersize=3, label = 'Queens')
    gbron.plot(ax = ax, marker='v', color='salmon', markersize=3, label = 'Bronx')
    ax.set_title('Listings in New York City')
    plt.legend()
    plt.savefig('images/nyc_map.png')

    for i in top20_labels: 
        c = nyc[nyc['neighbourhood'] == i] 
        print(c[['neighbourhood', 'neighbourhood_group']].head(1)) 

    



    
