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

def nested_dictionary(data, col_name):
    unique_vals = set(data[col_name])
    subdatasets = dict()
    for i in unique_vals:
        subdatasets[i] = data[data[col_name] == i]
    return subdatasets

def grouped_roomtype_count(df, grouping_col, num):
    counts = df[grouping_col].value_counts()
    top_num = counts[:num]
    districts = top_num.index

    listing_count = df.groupby(['room_type', grouping_col]).agg({'room_type': 'count'})
    room_type_by_district = {}
    for i in sorted(set(df.room_type)):
        room_type_by_district[i] = {j:0 for j in districts}
    for i in districts:
        type_in_dist = set(df[df[grouping_col] == i]['room_type'])
        for j in type_in_dist:
            room_type_by_district[j][i] = listing_count.loc[(j, i)]['room_type']
    return room_type_by_district

def roomtype_count(df):
    listing_count = df.groupby(['room_type']).agg({'room_type': 'count'})
    room_type_by_district = {}
    for i in sorted(set(df.room_type)):
        room_type_by_district[i] = listing_count.loc[i]['room_type']/len(df)
    return room_type_by_district



if __name__ == "__main__":
    #NYC EDA
    print(nyc.info())
    print(nyc.describe())

    ##NYC EDA

    neighborhood_listing_count = nyc['neighbourhood'].value_counts()
    top20_nyc_neighborhoods = neighborhood_listing_count[:20]
    top20_labels = top20_nyc_neighborhoods.index
    
    print('Top 20 neighbourhoods in NYC: {0}'.format(list(top20_labels)))
    count = {}
    for i in list(set(nyc['neighbourhood_group'])):
        hoods = set(nyc[nyc['neighbourhood_group'] == i]['neighbourhood'])
        for j in list(hoods):
            if j in list(top20_labels):
                if i not in count:
                    count[i] = 1
                else: 
                    count[i] += 1

    print('The counts of how many top 20 neighborhoods within each borough: {0}'.format(count))



    print('Mean price of a listing in NYC: {0}'.format(nyc['price'].mean()))
    
    boroughs_dict = nested_dictionary(nyc, 'neighbourhood_group')
    for k,v in boroughs_dict.items():
        print('Mean price in {0}, NY: {1}'.format(k, v['price'].mean()))
    print('----------------------')
    for k,v in boroughs_dict.items():
        print('Min price in {0}, NY: {1}'.format(k, v['price'].min()))
    print('----------------------')
    for k,v in boroughs_dict.items():
        print('Max price in {0}, NY: {1}'.format(k, v['price'].max()))
    print('----------------------')

    for k,v in boroughs_dict.items():
        print('Mean availability in {0}, NY: {1} days'.format(k, v['availability_365'].mean()))
    print('----------------------')
    for k,v in boroughs_dict.items():
        print('Min availability in {0}, NY: {1} days'.format(k, v['availability_365'].min()))
    print('----------------------')
    for k,v in boroughs_dict.items():
        print('Max availability in {0}, NY: {1} days'.format(k, v['availability_365'].max()))
    print('----------------------')
        
    for k,v in boroughs_dict.items():
        print('Mean host listing count in {0}, NY: {1} '.format(k, v['calculated_host_listings_count'].mean()))
    print('----------------------')
    for k,v in boroughs_dict.items():
        print('Min host listing count in {0}, NY: {1} '.format(k, v['calculated_host_listings_count'].min()))
    print('----------------------')
    for k,v in boroughs_dict.items():
        print('Max host listing count in {0}, NY: {1} '.format(k, v['calculated_host_listings_count'].max()))
    print('----------------------')    

    manhattan = nyc[nyc['neighbourhood_group'] == 'Manhattan']
    not_manhattan = nyc[nyc['neighbourhood_group'] != 'Manhattan']

    print('''Mean and standard deviation of price in Manhatttan, NY is {0} and {1}'''
            .format(manhattan['price'].mean(), manhattan['price'].std()))

    
    print('''Mean and standard deviation of price in all other boroughs in NYC is {0} and {1}'''
            .format(not_manhattan['price'].mean(), not_manhattan['price'].std()))

    room_type_boro = grouped_roomtype_count(nyc, 'neighbourhood_group', 5)
    room_counts = roomtype_count(nyc)



    print('''The number of listings per host: min: {0}, mean: {1}, max: {2}'''.format(nyc['calculated_host_listings_count'].min(), nyc['calculated_host_listings_count'].mean(), nyc['calculated_host_listings_count'].max()))
    print('Total number of unique hosts: {0}'.format(len(nyc['host_id'].unique())))

    multi_listings = nyc[nyc['calculated_host_listings_count'] > 10]  
    
    print('The number of listings where host has more than 10 locations: {0}'.format(len(multi_listings)))
    print('The number of hosts with more than 10 listings: {0}'.format(len(multi_listings['host_id'].unique())))
    
    

    

