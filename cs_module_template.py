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
    print('Initialising')

def perform_updates(output_name):
    """
    Steps that take place every time a change is detected in the 
    city_io grid data
    """
    print('Performing updates')
    output_data={}
    r = requests.post(cityIO_post_url+output_name, data = json.dumps(output_data))
    print(r)

city='Budapest'
output_name='test_module' # the output will appear on cityI/O as .../output_name

configs=json.load(open('./python/configs.json'))
city_configs=configs[city]

table_name=city_configs['table_name']
host='https://cityio.media.mit.edu/'

cityIO_get_url=host+'api/table/'+table_name
cityIO_post_url=host+'api/table/update/'+table_name+'/'

SLEEP_TIME=0.5 # seconds to sleep between checkinh cityI/O

CITYIO_SAMPLE_PATH='./'+city+'/sample_cityio_data.json'
META_GRID_SAMPLE_PATH='./'+city+'/sample_meta_grid.geojson'

# =============================================================================
# Get cityIO data for initialisation
# =============================================================================


try:
    with urllib.request.urlopen(cityIO_get_url+'/header/spatial') as url:
    #get the latest grid data
        cityIO_spatial_data=json.loads(url.read().decode())
except:
    print('Using static cityIO grid file')
    cityIO_data=json.load(open(CITYIO_SAMPLE_PATH))
    cityIO_spatial_data=cityIO_data['header']['spatial']


# Full meta grid geojson      
try:
    with urllib.request.urlopen(cityIO_get_url+'/meta_grid') as url:
    #get the meta_grid from cityI/O
        meta_grid=json.loads(url.read().decode())
except:
    print('Using static meta_grid file for initialisation')
    meta_grid=json.load(open(META_GRID_SAMPLE_PATH))
    
# Interactive cell to meta_grid geojson      
int_to_meta_grid={}
for fi, f in enumerate(meta_grid['features']):
    if f['properties']['interactive']:
        int_to_meta_grid[int(f['properties']['interactive_id'])]=fi


initialise()
    

# =============================================================================
# Interactive Analysis
# =============================================================================

lastId=0
while True:
#check if grid data changed
    try:
        with urllib.request.urlopen(cityIO_get_url+'/meta/hashes/grid') as url:
            hash_id=json.loads(url.read().decode())
    except:
        print('Cant access cityIO')
        hash_id=1
    if hash_id==lastId:
        sleep(SLEEP_TIME)
    else:
        try:
            with urllib.request.urlopen(cityIO_get_url+'/grid') as url:
                cityIO_grid_data=json.loads(url.read().decode())
        except:
            print('Using static cityIO grid file')
            cityIO_data=json.load(open(CITYIO_SAMPLE_PATH))  
            cityIO_grid_data=cityIO_data['grid']
        lastId=hash_id
        perform_updates(output_name)
        sleep(SLEEP_TIME) 
# =============================================================================
# =============================================================================
