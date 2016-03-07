#! /usr/local/bin/python

"""
Created on Thu Feb 11 2016

@author: lgarzio
"""

import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import numpy as np

'''
This script is used to generate timeseries plots from netCDF or ncml files.
'''

ncml = 'http://opendap-devel.ooi.rutgers.edu:8090/thredds/dodsC/first-in-class/Global_Irminger_Sea/GI01SUMO/06-METBKA000/recovered_host/GI01SUMO-SBD11-06-METBKA000-metbk_a_dcl_instrument_recovered-recovered_host/GI01SUMO-SBD11-06-METBKA000-metbk_a_dcl_instrument_recovered-recovered_host.ncml'
f = nc.Dataset(ncml)

global fName
head, tail = os.path.split(ncml)
fName = tail.split('.', 1)[0]

# Gets the time variable and converts to a date
time_var = f.variables['time']
time_num = time_var[:]
time_num_units = time_var.units
time = nc.num2date(time_num, time_num_units)

for v in f.variables:
    print v

    y_var = f.variables[v]
    y_data = y_var[:]

    # Skips the rest of the script if there are no unique values (e.g., array of nans)
    if len(np.unique(y_data)) == 1:
        print "One value. Continuing"
        continue

    # Skips the rest of the script if there is no unit attribute for the variable
    try:
        y_units = y_var.units
    except AttributeError:
        y_units = ""
        continue

    try:
        ymin = np.nanmin(y_data)
    except TypeError:
        ymin = ""
        continue

    try:
        ymax = np.nanmax(y_data)
    except TypeError:
        ymax = ""
        continue

    fig, ax = plt.subplots()
    plt.grid()
    try:
        plt.scatter(time, y_data, c='r', marker='o', lw = .25)
    except ValueError:
        print 'x and y must be the same size'
        continue

    # Format date axis
    df = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(df)
    fig.autofmt_xdate()
    #plt.xticks(rotation='horizontal')

    # Labels
    ax.set_ylabel(f[v].name + " ("+ y_units + ")")
    ax.set_title(fName, fontsize=9)
    ax.legend(["Max: %f" % ymax + "\nMin: %f" % ymin], loc='best', fontsize=8)

    save_dir = '/Users/lgarzio/Documents/OOI/DataReviews/firstinclass/GI01SUMO/GI01SUMO-SBD11-06-METBKA000'
    filename = fName + "_" + v
    save_file = os.path.join(save_dir, filename)  # create save file name
    plt.savefig(str(save_file),dpi=150) # save figure
    plt.close()