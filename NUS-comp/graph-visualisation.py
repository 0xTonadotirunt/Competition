
#scatterplot w animations and mapplot (plotly)
import numpy as np
def animate_map(time_col):
    fig = px.scatter_mapbox(trunc_df,
              lat="rawlat" ,
              lon="rawlng",
              hover_name="trj_id",
              color="speed",
              animation_frame=time_col,
              mapbox_style='carto-positron',
              category_orders={
              time_col:list(np.sort(df_formatted[time_col].unique()))
              },                  
              zoom=10)
    fig.show();
animate_map(time_col='pingtimestamp')

#mattplotlib with layering
import matplotlib.pyplot as plt




# Import image of Singapore
singapore_img = plt.imread('img/singapore_image.png')

# Create fig and ax
fig, ax = plt.subplots(figsize=(18,12)) # Configure the combined figure size of all subplots

# Generate scatter plot
scatter_plot_obj = ax.scatter(long, lat, cmap=plt.get_cmap("jet"), alpha=0.4)

# Set the title of the plot
plt.title('trj', fontsize=20)

# Set the ylabel and xlabel of plot
plt.ylabel('Latitude', fontsize=20)
plt.xlabel('Longitude', fontsize=20)

# Create the legend
cbar = plt.colorbar(mappable=scatter_plot_obj, ax=ax)

# Show the Singapore map
plt.imshow(singapore_img, extent=[103.5, 104, 1.15, 1.50], alpha=0.5)

# Display scatterplot
plt.show()
