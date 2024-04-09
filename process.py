"""
Downloads requisite data from NOAA.

Assumes a base directory which is https://downloads.psl.noaa.gov/Datasets/noaa.oisst.v2.highres/.
"""

import argparse
from tqdm import tqdm
from pathlib import Path
import netCDF4 as nc
import torch

# Parse the command-line arguments
parser = argparse.ArgumentParser(description='Process data from NOAA.')

# Save directory
parser.add_argument('--download_dir', type=str, help='Directory to find the downloaded files')
parser.add_argument('--save_dir', type=str, help='Directory to save the files')

args = parser.parse_args()

try:
    download_dir = Path(args.download_dir)
except:
    raise ValueError("Please provide a valid download directory")

try:
    save_dir = Path(args.save_dir)
except:
    raise ValueError("Please provide a valid save directory")

list_of_netcdf_files = list(download_dir.glob("sst.day.*"))

MAX_VALUE = 45
MIN_VALUE = -3

for file in tqdm(list_of_netcdf_files, desc="Processing files"):
    nc_dataset = nc.Dataset(file)

    torch_tensor = torch.tensor(nc_dataset.variables['sst'][:])
    torch.save(torch_tensor, save_dir / f"{file.name}.pt")

    # Normalise data
    torch_tensor = (torch_tensor - MIN_VALUE) / (MAX_VALUE - MIN_VALUE)
    
    torch.save(torch_tensor, save_dir / f"{file.name[:-3]}_normalised.pt")