import requests
import zipfile
import pandas as pd
import geopandas as gp
import matplotlib.pyplot as plt

def download_extract(url):
    response = requests.get(url)

    print(response.headers)

    fname = response.headers['Content-Disposition'].split('=')[1]

    if response.ok:
        with open(fname, 'wb') as f:
            f.write(response.content)
    print('-----------------')
    print(f'Downloaded {fname}')

    zipfile.ZipFile(fname, 'r').extractall('.')

def poverty_data(skip=3):
    return pd.read_csv('API_SI.POV.DDAY_DS2_en_csv_v2_10474275.csv', skiprows=skip)

def get_poverty(codes=['ARG', 'CIV', 'USA']):
    ls = {}

    for code in codes:
        ls[code] = pd.Series(poverty_data()[poverty_data()['Country Code'] == code].iloc[0][4:-1])

    rs = pd.concat(ls, axis=1, keys=codes).dropna(how='all')

    return rs.fillna(rs.mean())

def top_10_poverty_countries(year):
    rs = poverty_data().sort_values(year, ascending=False)[:10][['Country Name', year]]

    rs.index = rs['Country Name']

    return rs

def get_internet_for_country(year = '2016', codes=['AUT', 'BEL', 'DEU', 'DNK', 'ESP', 'FIN', 'GBR', 'GRC', 'HUN', 'ITA', 'LUX', 'NLD', 'POL', 'PRT', 'SWE']):
    it_data = pd.read_csv('API_IT.NET.USER.ZS_DS2_en_csv_v2_10475039.csv', skiprows=3)

    eu = gp.read_file(gp.datasets.get_path('naturalearth_lowres'))

    eu = eu[eu['iso_a3'].isin(codes)]

    wdata = it_data[it_data['Country Code'].isin(codes)].sort_values(year)[year].dropna()

    for i in range(len(wdata)):
        eu.loc[eu.index[i], year] = wdata.iloc[i]

    return eu.sort_values(year)
