# noaa-sst-data

Small repository for converting NOAA SST data to usable data for PyTorch.

## Usage

Begin by creating a python virtual environment

```
python3 -m venv noaa-sst-data-venv
source noaa-sst-data-venv/bin/activate
pip install -r requirements.txt --no-cache-dir
```

Then download the required files from the NOAA website through the following command (I have provided a default base link which works as of the 9th of April 2024)

```
python download.py --save_dir [PATH_TO_SAVE_DIR] (--base_url [NEW URL IF NEEDED])
```

This should have downloaded the necessary NetCDF files to a directory of your choosing. Now we need to convert them to PyTorch tensors. One can do this using the following command:

```
pyton process.py --download_dir [PATH_TO_SAVE_DIR] --save_dir [PATH_TO_FINAL_DIR]
```

This will save regular and normalised versions of the yearly data to PATH_TO_FINAL_DIR.

## Visualisation

One can use the code to create GIFs as well using visualisation.py. For example, here is a low-resolution GIF of the data from the year 2002.

![gif_of_2002](https://github.com/jackmiller2003/noaa-sst-data/assets/41097620/ab8e7e4f-d07d-4590-9e82-2731841ccba5)
