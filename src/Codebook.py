# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels as sm
import branca.colormap as cmp
import folium
import shapely
import plotly.express as px

# Canada, Quebec City Dataframe (Main City)
df=pd.read_csv('../data/canada/listings.csv')

# Remove coloumn 'neighbourhood_group' and 'license'  because it's all NaN
df.drop(['neighbourhood_group','license'], axis=1, inplace=True)

# Show the shape
df.shape

# Sample 10 Rows
df.head(10)

# Sorts and ranks neighborhood by mean price 
neig = df[['price','neighbourhood']].groupby('neighbourhood').mean()
neig = neig.sort_values('price')
neig['rank'] = np.arange(len(neig)) + 1
neig = neig.reset_index(level=0)



# Mapping without folium 

# Set bounds
BBox = ((df.longitude.min(),   df.longitude.max(), df.latitude.min(), df.latitude.max()))
# Import Image
ruh_m = plt.imread('../data/canada/map.png')
# Plot Data on Map (Draft v1)
fig, ax = plt.subplots(figsize = (8,7))
ax.scatter(df.longitude, df.latitude, zorder=1, alpha= 0.2, c='b', s=10)
ax.set_title('Plotting Spatial Data on Quebec Map')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')



# Mapping with folium + heatmap

map_osm = folium.Map(location=[df['latitude'].mean() , df['longitude'].mean()] , zoom_start=10)
temp = df[df['price'] < 500]
obs = list(zip(temp['latitude'], temp['longitude'], temp['price']))
room_types = df['room_type'].unique()
color_dict = dict(zip(room_types, list(colors.cnames.values())[0:len(room_types)]))
linear = cmp.LinearColormap(['yellow','green', 'purple'], vmin = df.price.min(), vmax=500)
for el in obs:
    folium.Circle(el[0:2], radius=4, color=linear(el[2]), opacity=0.2).add_to(map_osm)
map_osm



# Room Type Bar Plot

plot3=sns.barplot(x='room_type', y='price',data=df)
plot3.set(xlabel='Room Type', ylabel='Average Price',title='Room Type Average Price in Montreal')
plt.show()