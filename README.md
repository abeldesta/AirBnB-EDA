# Airbnb EDA in New York City Vs. Madrid
Capstone 1 project for Galvanize Data Science Immersive, Week 4 </br>
*By Abel Desta* 

# Introduction

## Data 
I found this dataset on kaggle, which was sourced from [InsideAirbnb](http://insideairbnb.com/index.html). The website is an independent, non-commercial set of tools and data that allows you to explore how Airbnb is really being used in cities around the world. 

The dataset for this project is Airbnb data for New York City and Madrid. Combined it contains 69732 listings within 16 columns. 


## Goals 
- Demonstrate my EDA, statistical analysis and visualization skills.
- Explore the Airbnb dataset for an opportunity to compare the New York City and Madrid markets, use a hypothesis test if warranted.

## Data Description 
If you looking for an updated verison of New York City, Madrid, or other Airbnb cities it can be found at [InsideAirbnb](http://insideairbnb.com/get-the-data.html), which is updated every month or so. 

I only reviewed the listing.csv file because my computer had hard time processing the other files. The website linked above also has review and booking data files available for most cities.

Each listing had 16 attributes, 20837 listings in Madrid and 48895 listings in New York City
- Listing Id
- Name of the Listing 
- Host Id
- Host Name
- Neighbourhood Group - i.e. Boroughs or Districts
- Neighbourhood
- Latitude 
- Longitude
- Room Type - i.e.
    - Entire home/apartment 
    - Private Room
    - Shared Room
    - Hotel Room
- Price
- Minimum Nights
- Number of Reviews 
- Reviews Per Month
- Calculated Host Listings Count
- Availability (Days)

# Exploratory Data Anaysis
I first wanted to get an understanding of each city before getting into anything else.

### NYC


<p align="center">
    <img src="images/borough_nyc.png" width='400' />
    <img src="images/top20_neighbourhood_nyc.png" width = '400' />
</p>

**Figure 1. Frequency of listings in each borough and the top 20 neighborhoods.**


The first couple things that interested me was the frequency of listings in each borough and the top 20 neighborhoods. In the left chart you see that Brooklyn and Manhattan are by far listing location. Which is not surprising since all main tourist attractions, such as sporting events, landmarks, and popular parks, are mostly located in those two boroughs. 

In the right chart you see the same graph but the frequency is grouped by neighbourhoods. One aspect I wanted to find from this graph is how many neighborhoods each of the boroughs had in the top 20. 

| Borough | Neighborhood Count |
| ------- | ------------------ |
| Manhattan | 12 |
| Brooklyn | 7 |
| Queens | 1 |
| Staten Island | 0 |
| Bronx | 0 |

**Table 1. Number of neighborhoods in top 20.**

Digging deeper into the listings in each borough, I wanted to see whether room types change depending on location. 

<p align="center">
    <img src="images/room_type_borough.png" />
<p/>

**Figure 2. Frequency of each room type separated by borough.**

Here you see that entire homes or apartment are the most popular for host listing in Manhattan, where as in every other borough private rooms are the most popular host listing. Shared rooms are the least common room type across all boroughs. 

There were three other columns I spent some time looking into: Price, Calculated Host Listings Count, Availablity

#### Price 

| Borough | Min Price | Mean Price | Max Price |
| ------- | --------- | ---------- | --------- |
| Manhattan | 0 | 196.87 | 10000 |
| Brooklyn | 0 | 124.38 | 10000 |
| Queens | 10 | 99.52 | 10000 |
| Staten Island | 13 | 114.81 | 5000 |
| Bronx | 0 | 87.50 | 2500 |

**Table 2. Minimum, Mean, and Maximum prices in each borough.**

There is not surprise that Brooklyn and Manhattan are the most expensive borough for bookings in New York City. A few thing I found interesting is that were the extreme outliers in Manhattan, Brooklyn and Queens each having a listing worth $10,000. Queens is the second cheapest borough from this dataset which makes it more surprising. On the same note, Staten Island is the popular location in terms of host listings yet its mean price is only $10 dollars cheaper than Brooklyn. 

#### Host Listing Count

| Area | Min Count | Mean Count | Max Count |
| ------- | --------- | ---------- | --------- |
| Manhattan | 1 | 13 | 327 |
| Brooklyn | 1| 2 | 232 |
| Queens | 1 | 4 | 103 |
| Staten Island | 1 | 2 | 8 |
| Bronx | 1 | 2| 37 |
| NYC | 1 | 7.14 | 327 |

**Table 3. Minimum, Mean, and Maximum number of listings in New York City.**

I thought it would be interesting to look into the number of listings each host had because Airbnb started as a company that helped people make extra cash on their primary property when they went on vacation or had an extra room a person could staying in while on vacation. I found that mean number of listings is about 7 in New York City. That number is heavyily skewed by upper 25th percentile because the 75th percentile is 2 listings per host and a standard deviation of 33 listings. When digging in deeper into the host with a count over 10 listings, I found that most host posting the listings were hotels like companys or small scale real estate investors.  

#### Availability 

| Borough | Mean Days | 
| ------- | --------- |
| Manhattan | 112 |
| Brooklyn | 100 | 
| Queens | 144.45 | 
| Staten Island | 200 | 
| Bronx | 166 |

**Table 4. Minimum, Mean, and Maximum days a listing is available for booking in each borough.**

I wanted to look in to availability thru out the year to see if the host complied with the Airbnb "rules". Supposed a host is not allowed to post a property where they do not spend more than 6 months a year. Based on my EDA until this point, I'm sure Airbnb doesnt enforce this "rule". When I check the mean number of days the listings were able to be booked Manhattan and Brooklyn were approximately available for booking 3-4 months out of the year. The other three borough were available about 6 months out of the year, I would assume that is the case because of the lack of popularity in these areas. 






    