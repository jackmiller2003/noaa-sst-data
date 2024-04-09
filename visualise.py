import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import imageio
import tempfile
import os
from tqdm import tqdm

def create_sst_gif(nc_file_path, gif_output_path):
    """
    From GPT-4.
    """
    # Load the NetCDF file
    dataset = nc.Dataset(nc_file_path, 'r')
    
    # Extract necessary data
    lat = dataset.variables['lat'][:][0]
    lon = dataset.variables['lon'][:][0]
    
    # Prepare a temporary directory to save the images
    temp_dir = tempfile.mkdtemp()

    lon = dataset.variables['lon'][:]
    lat = dataset.variables['lat'][:]
    length_of_file = len(dataset.variables['sst'])
    
    # Plot the data for each time step and save as images
    image_files = []
    for i in tqdm(range(length_of_file//2), desc="Creating images"):
        
        sst = dataset.variables['sst'][i][::2,::2]
        lon = dataset.variables['lon'][::2]
        lat = dataset.variables['lat'][::2]

        
        plt.figure(figsize=(10, 6))
        plt.pcolormesh(lon, lat, sst, shading='auto')
        plt.title(f'Sea Surface Temperature on Day {i+1}')
        plt.colorbar(label='SST (°C)')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        
        # Save each figure as an image file
        image_file = os.path.join(temp_dir, f"image_{i}.png")
        plt.savefig(image_file)
        plt.close()
        image_files.append(image_file)
    
    # Compile images into a GIF
    with imageio.get_writer(gif_output_path, mode='I') as writer:
        for image_file in tqdm(image_files, desc="Creating GIF"):
            image = imageio.imread(image_file)
            writer.append_data(image)
    
    # Clean up: remove the temporary images
    for image_file in image_files:
        os.remove(image_file)
    os.rmdir(temp_dir)  # Remove the temporary directory