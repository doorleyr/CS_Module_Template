#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 12:04:07 2019

@author: doorleyr
"""

from time import sleep
import json
import urllib
import requests

def initialise():
    """
    Steps that only need to be performed once when the model starts running
    """
    pass

def perform_updates(output_name):
    """
    Steps that takeplace every time a change is deteded in the city_io grid data
    """
    output_data={}
    r = requests.post(cityIO_output_path+output_name, data = json.dumps(output_data))
    print(r)

city='Budapest'

configs=json.load(open('./python/configs.json'))
city_configs=configs[city]

table_name=city_configs['table_name']
host='https://cityio.media.mit.edu/'

cityIO_grid_url=host+'api/table/'+table_name
cityIO_output_path=host+'api/table/update/'+table_name+'/'

CITYIO_SAMPLE_PATH='./'+city+'/sample_cityio_data.json'

# =============================================================================
# Get cityIO data for initialisation
# =============================================================================

try:
    with urllib.request.urlopen(cityIO_grid_url+'/header/spatial') as url:
    #get the latest grid data
        cityIO_spatial_data=json.loads(url.read().decode())
except:
    print('Using static cityIO grid file')
    cityIO_data=json.load(open(CITYIO_SAMPLE_PATH))
    cityIO_spatial_data=cityIO_data['header']['spatial']

# Interactive grid geojson    
try:
    with urllib.request.urlopen(cityIO_grid_url+'/grid_interactive_area') as url:
    #get the latest grid data
        grid_interactive=json.loads(url.read().decode())
except:
    print('Using static cityIO grid file')
    cityIO_data=json.load(open(CITYIO_SAMPLE_PATH))
    grid_interactive=cityIO_data['grid_interactive_area']
    
# Full table grid geojson      
try:
    with urllib.request.urlopen(cityIO_grid_url+'/grid_full_table') as url:
    #get the latest grid data
        grid_full_table=json.loads(url.read().decode())
except:
    print('Using static cityIO grid file')
    cityIO_data=json.load(open(CITYIO_SAMPLE_PATH))
    grid_full_table=cityIO_data['grid_full_table']


initialise()
    

# =============================================================================
# Interactive Analysis
# =============================================================================

lastId=0
while True:
#check if grid data changed
    try:
        with urllib.request.urlopen(cityIO_grid_url+'/meta/hashes/grid') as url:
            hash_id=json.loads(url.read().decode())
    except:
        print('Cant access cityIO')
        hash_id=1
    if hash_id==lastId:
        sleep(1)
    else:
        try:
            with urllib.request.urlopen(cityIO_grid_url+'/grid') as url:
                cityIO_grid_data=json.loads(url.read().decode())
        except:
            print('Using static cityIO grid file')
            cityIO_data=json.load(open(CITYIO_SAMPLE_PATH))  
            cityIO_grid_data=cityIO_data['grid']
        lastId=hash_id
        perform_updates('output_name')
        sleep(1) 
# =============================================================================
# =============================================================================
