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
import re

'''
This script is used to generate timeseries plots from netCDF or ncml files.
'''

ncml = 'http://opendap-devel.ooi.rutgers.edu:8090/thredds/dodsC/lgarzio-eval/Global_Station_Papa/GP02HYPM/04-CTDPFL000/telemetered/GP02HYPM-WFP02-04-CTDPFL000-ctdpf_ckl_wfp_instrument-telemetered/GP02HYPM-WFP02-04-CTDPFL000-ctdpf_ckl_wfp_instrument-telemetered.ncml'
f = nc.Dataset(ncml)

global fName
head, tail = os.path.split(ncml)
fName = tail.split('.', 1)[0]

# Gets the time variable and converts to a date
time_var = f.variables['time']
time_num = time_var[:]
time_num_units = time_var.units
time = nc.num2date(time_num, time_num_units)

# Identifies variables to skip when plotting
misc_vars = ['quality', 'string', 'timestamp', 'deployment', 'id', 'provenance', 'qc']
reg_ex = re.compile('|'.join(misc_vars))

sci_vars = [s for s in f.variables if not reg_ex.search(s)]

for v in sci_vars:
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
    #plt.xticks(rotation='vertical')

    # Labels
    ax.set_ylabel(f[v].name + " ("+ y_units + ")")
    ax.set_title(fName, fontsize=9)
    ax.legend(["Max: %f" % ymax + "\nMin: %f" % ymin], loc='best', fontsize=8)

    save_dir = '/Users/lgarzio/Documents'
    filename = fName + "_" + v
    save_file = os.path.join(save_dir, filename)  # create save file name
    plt.savefig(str(save_file),dpi=150) # save figure
    plt.close()