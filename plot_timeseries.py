#! /usr/local/bin/python

"""
Created on Thu Feb 11 2016

@author: lgarzio
"""

import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import os
import numpy as np
import re
import datetime

'''
This script is used to generate timeseries plots from netCDF or ncml files, between a time range specified by the user.
'''

def createDir(newDir):
    # Check if dir exists.. if it doesn't... create it. From Mike S
    if not os.path.isdir(newDir):
        try:
            os.makedirs(newDir)
        except OSError:
            if os.path.exists(newDir):
                pass
            else:
                raise

def plot_timeseries(t, y, ymin, ymax, args):

    yD = y.data

    fig, ax = plt.subplots()
    plt.grid()
    plt.margins(y=.1, x=.1)
    plt.plot(t, yD, c='r', marker='o', lw = .75)

    # Format date axis
    df = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(df)
    fig.autofmt_xdate()

    # Format y-axis to disable offset
    y_formatter = ticker.ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(y_formatter)

    # Labels
    ax.set_ylabel(args[1] + " ("+ y.units + ")")
    ax.set_title(args[0], fontsize=9)
    ax.legend(["Max: %f" % ymax + "\nMin: %f" % ymin], loc='best', fontsize=8)

    filename = args[0] + "_" + args[1]
    save_file = os.path.join(dir1, filename)  # create save file name
    plt.savefig(str(save_file),dpi=150) # save figure
    plt.close()


save_dir = '/Users/lgarzio/Documents/OOI/DataReviews/restinclass/Endurance'

urls = ['http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/05-CTDGVM000/recovered_host/CE05MOAS-GL319-05-CTDGVM000-ctdgv_m_glider_instrument_recovered-recovered_host/CE05MOAS-GL319-05-CTDGVM000-ctdgv_m_glider_instrument_recovered-recovered_host.ncml',
        'http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/04-DOSTAM000/recovered_host/CE05MOAS-GL319-04-DOSTAM000-dosta_abcdjm_glider_recovered-recovered_host/CE05MOAS-GL319-04-DOSTAM000-dosta_abcdjm_glider_recovered-recovered_host.ncml',
        'http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/02-FLORTM000/recovered_host/CE05MOAS-GL319-02-FLORTM000-flort_m_glider_recovered-recovered_host/CE05MOAS-GL319-02-FLORTM000-flort_m_glider_recovered-recovered_host.ncml',
        'http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/01-PARADM000/recovered_host/CE05MOAS-GL319-01-PARADM000-parad_m_glider_recovered-recovered_host/CE05MOAS-GL319-01-PARADM000-parad_m_glider_recovered-recovered_host.ncml']

# enter deployment dates
start_time = datetime.datetime(2014, 04, 01, 0, 0, 0)
end_time = datetime.datetime(2014, 05, 29, 0, 0, 0)


# Identifies variables to skip when plotting
misc_vars = ['quality', 'string', 'timestamp', 'deployment', 'id', 'provenance', 'qc',  'time', 'mission', 'obs',
            'volt', 'ref', 'sig', 'amp', 'rph', 'calphase', 'phase', 'therm']
reg_ex = re.compile('|'.join(misc_vars))


for url in urls:
    print url
    f = xr.open_dataset(url)
    f = f.swap_dims({'obs':'time'})
    f_slice = f.sel(time=slice(start_time,end_time)) # select only deployment dates provided
    fN = f_slice.source
    global fName
    head, tail = os.path.split(url)
    fName = tail.split('.', 1)[0]
    title = fName[0:27]
    platform1 = title.split('-')[0]
    platform2 = platform1 + '-' + title.split('-')[1]
    method = fName.split('-')[-1]
    dir1 = os.path.join(save_dir, platform1, platform2, title, method, 'timeseries_' + str(start_time.date()) + '_to_' + str(end_time.date()))
    createDir(dir1)
    t = f_slice['time'].data


    varList = []
    for vars in f_slice.variables:
        varList.append(str(vars))

    yVars = [s for s in varList if not reg_ex.search(s)]

    for v in yVars:
        print v

        y = f_slice[v]
        yD = y.data

        try:
            ymin = np.nanmin(yD)
        except TypeError:
            ymin = ""
            continue

        try:
            ymax = np.nanmax(yD)
        except TypeError:
            ymax = ""
            continue

        plotArgs = (fName, v)
        plot_timeseries(t, y, ymin, ymax, plotArgs)