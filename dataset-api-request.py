# Download Selected Parts of the ERA5 Dataset
#
#
# Reference: https://doi.org/10.24381/cds.f17050d7


import cdsapi
from datetime import datetime as dt


# User
year_first = 1985


# Let cdsapi handle the authentication, etc.
c = cdsapi.Client()


# Get current date and time
now = dt.now()
years = [f'{year}' for year in range(year_first, now.year)]

# Download data for everymonth until last year
c.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
        'product_type': 'monthly_averaged_reanalysis',
        'variable': 'skin_temperature',
        'year': years,
        'month': [f'{month:02d}' for month in range(1,13)],
        'time': '00:00',
        'format': 'netcdf',
    },
    f'data-{year_first}-to-{now.year-1}.nc')


# Check if we can download any data based on current date
if now.month < 2:
    print(f"error: too early to fetch <{now.year}> data")
    exit(0)


# Download this year's data up to where available
c.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
        'product_type': 'monthly_averaged_reanalysis',
        'variable': 'skin_temperature',
        'year':  [f'{now.year}'],
        'month': [f'{month:02d}' for month in range(1,now.month)],
        'time': '00:00',
        'format': 'netcdf',
    },
    f'data-{now.year}.nc')
