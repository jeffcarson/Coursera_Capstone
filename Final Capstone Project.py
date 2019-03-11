
# coding: utf-8

# Import Libraries

# In[1]:


import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

get_ipython().system(u'conda install -c conda-forge geopy --yes ')
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

get_ipython().system(u'conda install -c conda-forge folium=0.5.0 --yes')
import folium # plotting library

print('Folium installed')
print('Libraries imported.')


# Establish Foursquare Crendentials

# In[2]:


CLIENT_ID = 'PNWC3UG1LGIJTROW0HJZYEIFMBJ5RRC2PCCD2UMSZYKNQQKD' # your Foursquare ID
CLIENT_SECRET = '4GAGO34R0KVAL5VFESIDOPYB1EQ4CIJNVAM2MEOHOKPDIJP4' # your Foursquare Secret
VERSION = '20180604'
LIMIT = 60
print('Your credentials:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# Convert Address Into Latitude and Longitude and Set Radius

# In[6]:


#Pick center point of Dallas (Dallas City Hall)
address = '1500 Marilla St, Dallas, TX 75201'
geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)
#radius is in meters. Dallas is approximately 385.8 square miles = 19.64 miles.  1 mile = 1,609.64 meters therefore 19.64 miles = approximately 31,611 meters. 
radius = 31611


# Define URL

# In[7]:


#(1) Farmers Market, (2) Fish Market (3) Grocery Store (4) Health Food Store (5) Organic Grocery (6) Supermarket (7) Fruit & Vegetable Store (8) Fast Food Restaurant (9) Convenience Store
url1 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&categoryId=4bf58dd8d48988d1fa941735&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude,VERSION, radius, LIMIT)
url2 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&categoryId=4bf58dd8d48988d10e951735&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude,VERSION, radius, LIMIT)
url3 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&categoryId=4bf58dd8d48988d118951735&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude,VERSION, radius, LIMIT)
url4 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&categoryId=50aa9e744b90af0d42d5de0e&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude,VERSION, radius, LIMIT)
url5 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&categoryId=52f2ab2ebcbc57f1066b8b45&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude,VERSION, radius, LIMIT)
url6 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&categoryId=52f2ab2ebcbc57f1066b8b46&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude,VERSION, radius, LIMIT)
url7 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&categoryId=52f2ab2ebcbc57f1066b8b1c&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude,VERSION, radius, LIMIT)
url8 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&categoryId=4bf58dd8d48988d16e941735&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude,VERSION, radius, LIMIT)
url9 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&categoryId=4d954b0ea243a5684a65b473&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude,VERSION, radius, LIMIT)
url10 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&categoryId=4bf58dd8d48988d186941735&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude,VERSION, radius, LIMIT)


# Generate JSON File

# In[55]:


#generate JSON File
import requests
results = requests.get(url10).json()
#results
'There are {} around Dallas City Hall.'.format(len(results['response']['venues']))


# In[56]:


#get relevant part of JSON
results2 = results['response']['venues']

#transform results2 into a dataframe
dataframe = json_normalize(results2) # flatten JSON
#dataframe.head()


# In[57]:


# keep only columns that include venue name, and anything that is associated with location
filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['id']
dataframe_filtered = dataframe.loc[:, filtered_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']


# filter the category for each row
dataframe_filtered['categories'] = dataframe_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered.columns = [column.split('.')[-1] for column in dataframe_filtered.columns]

#dataframe_filtered


# Combining the 9 DataSets that were manually generated without a loop

# In[22]:


farmers_market = dataframe_filtered
farmers_market.dropna(subset=['city'], inplace=True)
farmers_market = farmers_market[(farmers_market['city'].str.contains('Dallas'))]
farmers_market.head()


# In[26]:


fish_market = dataframe_filtered
fish_market.dropna(subset=['city'], inplace=True)
fish_market = fish_market[(fish_market['city'].str.contains('Dallas'))]
fish_market.loc[fish_market['categories'] =='Seafood Restaurant', 'categories'] = 'Fish Market'
fish_market.head()


# In[30]:


grocery_store = dataframe_filtered
grocery_store.dropna(subset=['city'], inplace=True)
grocery_store = grocery_store[(grocery_store['city'].str.contains('Dallas'))]
grocery_store.loc[grocery_store['categories'] =='Big Box Store', 'categories'] = 'Grocery Store'
grocery_store.loc[grocery_store['categories'] =='Gourmet Shop', 'categories'] = 'Grocery Store'
grocery_store.head()


# In[34]:


health_food_store = dataframe_filtered
health_food_store.dropna(subset=['city'], inplace=True)
health_food_store = health_food_store[(health_food_store['city'].str.contains('Dallas'))]
health_food_store.loc[health_food_store['categories'] =='Gluten-free Restaurant', 'categories'] = 'Health Food Store'
health_food_store.loc[health_food_store['categories'] =='Supplement Shop', 'categories'] = 'Health Food Store'
health_food_store.head()


# In[38]:


organic_grocery = dataframe_filtered
organic_grocery.dropna(subset=['city'], inplace=True)
organic_grocery = organic_grocery[(organic_grocery['city'].str.contains('Dallas'))]
organic_grocery.head()


# In[42]:


supermarket = dataframe_filtered
supermarket.dropna(subset=['city'], inplace=True)
supermarket = supermarket[(supermarket['city'].str.contains('Dallas'))]
supermarket.loc[supermarket['categories'] =='Big Box Store', 'categories'] = 'Supermarket'
supermarket.head()


# In[46]:


fruit_and_veggie = dataframe_filtered
fruit_and_veggie.dropna(subset=['city'], inplace=True)
fruit_and_veggie = fruit_and_veggie[(fruit_and_veggie['city'].str.contains('Dallas'))]
fruit_and_veggie.head()


# In[50]:


fast_food = dataframe_filtered
fast_food.dropna(subset=['city'], inplace=True)
fast_food = fast_food[(fast_food['city'].str.contains('Dallas'))]
fast_food.loc[fast_food['categories'] =='Burger Joint', 'categories'] = 'Fast Food Restaurant'
fast_food.loc[fast_food['categories'] =='Fried Chicken Joint', 'categories'] = 'Fast Food Restaurant'
fast_food.head()


# In[54]:


convenience_store = dataframe_filtered
convenience_store.dropna(subset=['city'], inplace=True)
convenience_store = convenience_store[(convenience_store['city'].str.contains('Dallas'))]
convenience_store.loc[convenience_store['categories'] =='Pharmacy', 'categories'] = 'Convenience Store'
convenience_store.loc[convenience_store['categories'] =='Gas Station'] = 'Convenience Store'
convenience_store.head()


# In[58]:


liquor_store = dataframe_filtered
liquor_store.dropna(subset=['city'], inplace=True)
liquor_store = liquor_store[(liquor_store['city'].str.contains('Dallas'))]
liquor_store.loc[liquor_store['categories'] =='Wine', 'categories'] = 'Liquor Store'
liquor_store.head()


# In[62]:


all_stores = [farmers_market, fish_market, grocery_store, health_food_store, organic_grocery, supermarket, fruit_and_veggie, fast_food, convenience_store, liquor_store]

combined_stores = pd.concat(all_stores)


# In[82]:


#Drop Duplicate ID's
combined_stores.drop_duplicates(subset=['id'], keep=False)


# In[184]:


#List of Categories and Counts
temp_dataframe = combined_stores[['categories']]
category_counts = temp_dataframe.groupby(['categories']).size().reset_index(name='Total')
category_counts = category_counts.rename(columns={'categories': 'Venue Type'})
category_counts


# In[187]:


#List of Names and Counts
temp_dataframe = combined_stores[['name']]
name_counts = temp_dataframe.groupby(['name']).size().reset_index(name='Total')
name_counts = name_counts.rename(columns={'name': 'Name of Venue'})
name_counts


# In[202]:


#List of Zip Codes and Counts
temp_dataframe = combined_stores[['postalCode']]
zip_counts = temp_dataframe.groupby(['postalCode']).size().reset_index(name='Total')
zip_counts = zip_counts.rename(columns={'postalCode': 'Zip Code'})
zip_counts


# Cluster Lat and Long

# In[ ]:





#Plot Clusters
# Initialize the plot with the specified dimensions.
fig = plt.figure(figsize=(6, 4))

# Colors uses a color map, which will produce an array of colors based on
# the number of labels there are. We use set(k_means_labels) to get the
# unique labels.
colors = plt.cm.Spectral(np.linspace(0, 1, len(set(k_means_labels))))

# Create a plot
ax = fig.add_subplot(1, 1, 1)

# For loop that plots the data points and centroids.
# k will range from 0-3, which will match the possible clusters that each
# data point is in.
for k, col in zip(range(len([[4,4], [-2, -1], [2, -3], [1, 1]])), colors):

    # Create a list of all data points, where the data poitns that are 
    # in the cluster (ex. cluster 0) are labeled as true, else they are
    # labeled as false.
    my_members = (k_means_labels == k)
    
    # Define the centroid, or cluster center.
    cluster_center = k_means_cluster_centers[k]
        
    # Plots the datapoints with color col.
    ax.plot(FinalData[my_members, 0], FinalData[my_members, 1], 'w', markerfacecolor=col, marker='.')
    
    # Plots the centroids with specified color, but with a darker outline
    ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,  markeredgecolor='k', markersize=6)

# Title of the plot
ax.set_title('KMeans')

# Remove x-axis ticks
ax.set_xticks(())

# Remove y-axis ticks
ax.set_yticks(())

# Show the plot
plt.show()


# In[76]:


#Drop Categorical Variables and Create a Unique Key
FinalData = combined_stores[['lat','lng']]
FinalData['UniqueKey']=np.arange(len(FinalData))
FinalData


# In[78]:


from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans 
from sklearn.datasets.samples_generator import make_blobs 

#Normalize the Dataframe
Clus_dataSet = StandardScaler().fit_transform(FinalData)


# In[80]:


#Cluster the Dataset
clusterNum = 3
k_means = KMeans(init = "k-means++", n_clusters = clusterNum, n_init = 12)
k_means.fit(Clus_dataSet)
k_means_labels = k_means.labels_

#Assign Labels to each Row
FinalData["Clus_km"] = k_means_labels

#Get Coordinates of Cluster Centers
k_means_cluster_centers = k_means.cluster_centers_
#k_means_cluster_centers


# Visualize items on the map around our location

# In[86]:


venues_map = folium.Map(location=[latitude, longitude], zoom_start=13) # generate map centred around Dallas City Hall

# add a red circle marker to represent Dallas City Hall
folium.features.CircleMarker(
    [latitude, longitude],
    radius=4,
    color='grey',
    popup='Dallas City Hall',
    fill = True,
    fill_color = 'grey',
    fill_opacity = 1
).add_to(venues_map)

# add the Farmer's Market locations as blue circle markers
for lat, lng, label in zip(farmers_market.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        color='green',
        popup=label,
        fill = True,
        fill_color='green',
        fill_opacity=1
    ).add_to(venues_map)

        # add the Fish Market locations as green circle markers
for lat, lng, label in zip(fish_market.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        color='green',
        popup=label,
        fill = True,
        fill_color='green',
        fill_opacity=1
    ).add_to(venues_map)

        # add the Grocery Store locations as yellow circle markers
for lat, lng, label in zip(grocery_store.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        color='green',
        popup=label,
        fill = True,
        fill_color='green',
        fill_opacity=1
    ).add_to(venues_map)
    
        # add the Health Food Store locations as yellow circle markers
for lat, lng, label in zip(health_food_store.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
       radius=5,
        color='green',
        popup=label,
        fill = True,
        fill_color='green',
        fill_opacity=1
    ).add_to(venues_map)
    
        # add the Organic Grocery locations as yellow circle markers
for lat, lng, label in zip(organic_grocery.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        color='green',
        popup=label,
        fill = True,
        fill_color='green',
        fill_opacity=1
    ).add_to(venues_map)
    
        # add the Supermarket locations as yellow circle markers
for lat, lng, label in zip(supermarket.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        color='green',
        popup=label,
        fill = True,
        fill_color='green',
        fill_opacity=1
    ).add_to(venues_map)
    
        # add the Fruit & Vegetable Store locations as yellow circle markers
for lat, lng, label in zip(fruit_and_veggie.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        color='green',
        popup=label,
        fill = True,
        fill_color='green',
        fill_opacity=1
    ).add_to(venues_map)
    
        # add the Fast Food locations as yellow circle markers
for lat, lng, label in zip(fast_food.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
       color='red',
        popup=label,
        fill = True,
        fill_color='red',
        fill_opacity=1
    ).add_to(venues_map)
    
        # add the Convenience Store locations as yellow circle markers
for lat, lng, label in zip(convenience_store.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        color='red',
        popup=label,
        fill = True,
        fill_color='red',
        fill_opacity=1
    ).add_to(venues_map)
    
        # add the Liquor Store locations as yellow circle markers
for lat, lng, label in zip(liquor_store.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=5,
        color='black',
        popup=label,
        fill = True,
        fill_color='black',
        fill_opacity=1
    ).add_to(venues_map)

# display map
venues_map

