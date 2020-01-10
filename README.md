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
The first couple things that interested me was the frequency of listings in each borough and the top 20 neighborhoods.

![Frequency by Borough!]("images/borough.png")
<!-- <p align="center">
<img src="/images/borough.png">
<img src="/images/top20_neighbourhood_nyc.png">
</p> -->




    