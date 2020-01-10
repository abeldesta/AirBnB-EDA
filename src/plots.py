import pandas as pd 
import numpy as np 
import scipy.stats as stats
import random 
import matplotlib.pyplot as plt 
import geopandas 
import geoplot
import eda
plt.style.use('ggplot')


def bar_plot(data, labels, title = None, xlabel = None, ylabel = None):
    fig, ax = plt.subplots(1,1)
    width = 0.8
    tickLocals = np.arange(len(data))
    ax.barh(tickLocals, data[::-1], width, color = 'dodgerblue')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize = 12)
    ax.set_yticks(ticks = tickLocals)
    ax.set_yticklabels(labels[::-1])
    plt.tight_layout(pad=1)
    
def side_by_side_bar(d, title, xlabel, ylabel):
    fig, ax = plt.subplots(1,1)
    width = 0.2
    N = len(d) - 1
    for k, v in d.items():
        labels = v.keys()
        colors = {'Entire home/apt': 'dodgerblue', 'Private room': 'salmon', 'Hotel room': 'yellowgreen', 'Shared room': 'navajowhite'}
        tickLocals = np.arange(len(v))
        ax.bar(tickLocals-N*width, v.values(), width, color = colors[k], label = k)
        ax.set_xticks(ticks = tickLocals)
        ax.set_xticklabels(labels)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        # plt.xticks(rotation = 80)
        plt.legend()
        plt.tight_layout(pad=1)
        N -= 1

def geo_df(df, x = 'longitude', y = 'latitude'):
    return geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df[x], df[y]))

def nested_dictionary(data, col_name):
    unique_vals = set(data[col_name])
    subdatasets = dict()
    for i in unique_vals:
        subdatasets[i] = data[data[col_name] == i]
    return subdatasets

def geomap_plot(d, base_map, color_dict, title = None, labels = None):
    fig, ax = plt.subplots(1,1)
    ax.set_aspect('equal')
    base = base_map.plot(ax = ax, alpha=0.5, edgecolor='k')
    for k,v in d.items():
        v.plot(ax = ax, marker='.', c=color_dict[k], markersize=5, label = k)
    ax.set_title(title)
    if len(d) > 10:
        plt.legend(labels[:10])
    else: 
        plt.legend()

colors = ['dodgerblue', 'salmon', 'navajowhite', 'yellowgreen', 'mediumorchid', 'lawngreen', 'orange', 'forestgreen', 'darkmagenta',
          'crimson', 'darkgoldenrod', 'burlywood', 'aqua', 'lightcoral', "violet", 'red', 'green', 'teal', 'hotpink', 'silver', 'black', 'gold']

def color_dict(lst, df, col_name):
    vals = set(df[col_name])
    subset = random.sample(lst, k = len(vals))
    col_dict = {k: subset[idx] for idx, k in enumerate(vals)}
    return col_dict

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

    
def hist_plot(data, col_name):
    fig, ax = plt.subplots(1,1)
    ax.hist(data[col_name])
    plt.show()

def boxplot():
    pass


if __name__ == "__main__":
    #read in datasets
    nyc = pd.read_csv('data/nyc_data.csv')
    madrid = pd.read_csv('data/madrid_data.csv')


    #EDA plot
    borough_labels, borough_counts = eda.top_20(nyc, 'neighbourhood_group')
    neighborhood_labels, neighborhood_counts = eda.top_20(nyc, 'neighbourhood')
    bar_plot(borough_counts, borough_labels, 'Airbnb Frequency in NYC by Borough', 'Number of Listings', 'Boroughs')
    plt.savefig('images/borough_nyc.png')
    bar_plot(neighborhood_counts, neighborhood_labels, 'Airbnb Frequency in NYC by Neighborhood', 'Number of Listings', 'Neighborhoods')
    plt.savefig('images/top20_neighbourhood_nyc.png')
    
    room_type_by_borough_nyc = grouped_roomtype_count(nyc, 'neighbourhood_group', 5)
    side_by_side_bar(room_type_by_borough_nyc, 'Airbnb Room Type Frequency in NYC by Borough', 'Boroughs', 'Number of Listings')
    plt.savefig('images/room_type_borough.png')

    nyc_colors = {'Brooklyn': 'dodgerblue', 'Bronx': 'salmon', 'Manhattan': 'navajowhite', 'Staten Island': 'yellowgreen', 'Queens': 'mediumorchid'}
    nyc_map = geopandas.read_file('shapefiles/borough/geo_export_91122496-4899-4211-a64b-3cf55c0ddeae.shp')
    group_colors = color_dict(colors, nyc, 'neighbourhood_group')
    geo_nyc = geo_df(nyc)
    grouped_geo_df = nested_dictionary(geo_nyc, 'neighbourhood_group')
    geomap_plot(grouped_geo_df, nyc_map, nyc_colors, title = 'Airbnb Listings in New York City')
    plt.savefig('images/nyc_map.png')

    district_labels, district_counts = eda.top_20(madrid, 'neighbourhood_group')
    madrid_neighborhood_labels, madrid_neighborhood_counts = eda.top_20(madrid, 'neighbourhood')
    bar_plot(district_counts, district_labels, 'Airbnb Frequency in Madrid by District', 'Number of Listings', 'District')
    plt.savefig('images/district_madrid.png')
    bar_plot(madrid_neighborhood_counts, madrid_neighborhood_labels, 'Top 20 Airbnb Frequency in Madrid by Neighborhood', 'Number of Listings', 'Neighborhoods')
    plt.savefig('images/top5_madrid_neighborhoods.png')

    room_type_by_borough_madrid = grouped_roomtype_count(madrid, 'neighbourhood_group', 5)
    side_by_side_bar(room_type_by_borough_madrid, 'Airbnb Room Type Frequency in Madrid by Districts', 'Districts', 'Number of Listings')
    plt.savefig('images/room_type_districts.png')

    madrid_colors = color_dict(colors, madrid, 'neighbourhood_group')
    madrid_map = geopandas.read_file('shapefiles/Distritos/Distritos.shp')
    geo_madrid = geo_df(madrid)
    #Converting the coordinates reference system to the same as the shapefile
    #Longitude and Latitude to Mercator
    geo_madrid.crs = {'init': 'epsg:4326'}
    geo_madrid = geo_madrid.to_crs({'init': 'epsg:25830'})
    grouped_geo_df = nested_dictionary(geo_madrid, 'neighbourhood_group')
    labels, top20 = eda.top_20(madrid, 'neighbourhood_group')
    geomap_plot(grouped_geo_df, madrid_map, madrid_colors, title = 'Airbnb Listings in Madrid, Spain', labels = labels)
    plt.savefig('images/madrid_map.png')


    


