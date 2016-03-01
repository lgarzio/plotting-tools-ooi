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

#ncml = 'http://opendap-devel.ooi.rutgers.edu:8090/thredds/dodsC/ooiufs01/Cabled_Array/RS01SBPS/3A-FLORTD101/streamed/RS01SBPS-SF01A-3A-FLORTD101-flort_d_data_record-streamed/RS01SBPS-SF01A-3A-FLORTD101-flort_d_data_record-streamed.ncml'

ncml = 'http://opendap-devel.ooi.rutgers.edu:8090/thredds/dodsC/ufs-west/Global_Southern_Ocean/GS01SUMO/06-METBKA000/telemetered/GS01SUMO-SBD12-06-METBKA000-metbk_hourly-telemetered/GS01SUMO-SBD12-06-METBKA000-metbk_hourly-telemetered.ncml'
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

    #ymin = np.nanmin(y_data)
    #ymax = np.nanmax(y_data)

    fig, ax = plt.subplots()
    plt.grid()
    try:
        plt.scatter(time, y_data, c='r', marker='o')
    except ValueError:
        print 'x and y must be the same size'
        continue

    # Format date axis
    df = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(df)
    fig.autofmt_xdate()

    # Labels
    ax.set_ylabel(f[v].name + " ("+ y_units + ")")
    ax.set_title(fName, fontsize=9)
    #ax.legend(["Max: %f" % ymax + "\nMin: %f" % ymin], loc='best', fontsize=8)

    save_dir = '/Users/lgarzio/Documents/OOI/DataReviews/2016_2_19_westcoast/GS01SUMO/timeseries/GS01SUMO-SBD12-METBK/metbk_hourly'
    filename = fName + "_" + v
    save_file = os.path.join(save_dir, filename)  # create save file name
    plt.savefig(str(save_file),dpi=150) # save figure
    plt.close()