"""
Downloads requisite data from NOAA.

Assumes a base directory which is https://downloads.psl.noaa.gov/Datasets/noaa.oisst.v2.highres/.
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse
from tqdm import tqdm
from pathlib import Path


# The base URL containing the files you want to download
BASE_URL = 'https://downloads.psl.noaa.gov/Datasets/noaa.oisst.v2.highres/'

# Parse the command-line arguments
parser = argparse.ArgumentParser(description='Download data from NOAA.')

# Add an argument for the base URL
parser.add_argument('--base_url', type=str, default=BASE_URL, help='The base URL to download data from')

# Save directory
parser.add_argument('--save_dir', type=str, help='Directory to save the files')

args = parser.parse_args()

try:
    save_dir = Path(args.save_dir)
except:
    raise ValueError("Please provide a valid save directory")

# Use requests to fetch the content of the base URL
response = requests.get(args.base_url)
response.raise_for_status()  # Raises an error if the request failed

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

file_urls = []

for link in soup.find_all("a"):
    href = link.get("href")
    
    if "day.mean" in href:
        file_url = urljoin(args.base_url, href)
        file_urls.append(file_url)

for file_link in tqdm(file_urls, desc="Downloading files"):
    filename = file_link.split('/')[-1]

    response = requests.get(file_link)
    response.raise_for_status()

    path_to_save = save_dir / f"{filename}.nc"

    # Save the file to the current directory
    with open(path_to_save, 'wb') as file:
        file.write(response.content)