#! /usr/local/bin/python

"""
Created on Wed Aug 24 2016

@author: lgarzio
"""

import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.lines as mlines
import numpy as np
import os
import re
import datetime
import pandas as pd

'''
This script is used to create timeseries plots of telemetered and recovered data from netCDF or ncml files, by month,
between a time range specified by the user (must be <1 year).
"Overlay" plots plot telemetered and recovered data on top of each other by month, and provide min and max values.
"Panel" plots create 3 plots on one page
    1. The top plot is a re-created overlay plot, by month
    2. The middle plot is recovered data only, by month
    3. The bottom plot is telemetered data only, by month
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

def plot_timeseries_overlay(time_r, time_t, rD, tD, args):

    # get min and max for recovered and telemetered data
    rmin = np.nanmin(rD)
    rmax = np.nanmax(rD)
    tmin = np.nanmin(tD)
    tmax = np.nanmax(tD)

    fig, ax = plt.subplots()
    plt.grid()
    plt.margins(y=.1, x=.1)
    ax.plot(time_r, rD, 'o', markerfacecolor='none', markeredgecolor='r', lw=.75)  #plot recovered data
    ax.plot(time_t, tD, 'x', markeredgecolor='b', lw=1.5)  #plot telemetered data

    # Format date axis
    df = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(df)
    fig.autofmt_xdate()

    # Format y-axis to disable offset
    y_formatter = ticker.ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(y_formatter)

    # Labels
    ax.set_ylabel(args[0].name + " ("+ args[0].units + ")")
    title = args[1] + '_' + args[2] + args[3]
    ax.set_title(title, fontsize=10)

    # Format legend
    rec_leg = mlines.Line2D([], [], markerfacecolor='none', marker='o', markeredgecolor='r', color='r',
                            label=("Recovered" + "\n  Max: %f" % rmax + "\n  Min: %f" % rmin))
    rec_tel = mlines.Line2D([], [], marker='x', markeredgecolor='b', ls=':',
                            label=("Telemetered" + "\n  Max: %f" % tmax + "\n  Min: %f" % tmin))
    ax.legend(handles=[rec_leg, rec_tel],loc='best', fontsize=8)

    # Save plot
    filename = args[1] + "_" + args[0].name + "_" + args[3] + "month" + args[4] + "_overlay"
    save_file = os.path.join(args[5], filename)  # create save file name
    plt.savefig(str(save_file),dpi=150) # save figure
    plt.close()


def plot_timeseries_overlay_panel(time_r, time_t, rD, tD, args):

    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
    plt.margins(y=.1, x=.1)

    # plot recovered data
    ax1.plot(time_r, rD, 'o', markerfacecolor='none', markeredgecolor='r', lw=.75, label='recovered')
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(True)

    ax2.plot(time_r, rD, 'o', markerfacecolor='none', markeredgecolor='r', lw=.75, label='recovered')
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)

    # plot telemetered data
    ax1.plot(time_t, tD, 'x', markeredgecolor='b', lw=1.5, label='telemetered')
    ax3.plot(time_t, tD, 'x', markeredgecolor='b', lw=1.5, label='telemetered')
    ax3.xaxis.grid(True)
    ax3.yaxis.grid(True)

    # Format date axis
    df = mdates.DateFormatter('%Y-%m-%d')
    ax1.xaxis.set_major_formatter(df)
    fig.autofmt_xdate()

    # Format y-axis to disable offset
    y_formatter = ticker.ScalarFormatter(useOffset=False)
    ax1.yaxis.set_major_formatter(y_formatter)

     # Labels
    ax2.set_ylabel(args[0].name + " ("+ args[0].units + ")")
    title = args[1] + '_' + args[2] + args[3]
    ax1.set_title(title, fontsize=10)

    # Legends
    ax1.legend(loc='best', fontsize=6, markerscale=.5)
    ax2.legend(loc='best', fontsize=6, markerscale=.5)
    ax3.legend(loc='best', fontsize=6, markerscale=.5)

    # Save plot
    filename = args[1] + "_" + args[0].name + "_" + args[3] + "month" + args[4] + "_panel"
    save_file = os.path.join(args[5], filename)  # create save file name
    plt.savefig(str(save_file),dpi=150) # save figure
    plt.close()


save_dir = '/Users/lgarzio/Documents/OOI/DataReviews/restinclass/Endurance'

recovered = 'http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/05-CTDGVM000/recovered_host/CE05MOAS-GL319-05-CTDGVM000-ctdgv_m_glider_instrument_recovered-recovered_host/CE05MOAS-GL319-05-CTDGVM000-ctdgv_m_glider_instrument_recovered-recovered_host.ncml'
telemetered = 'http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/05-CTDGVM000/telemetered/CE05MOAS-GL319-05-CTDGVM000-ctdgv_m_glider_instrument-telemetered/CE05MOAS-GL319-05-CTDGVM000-ctdgv_m_glider_instrument-telemetered.ncml'

# enter deployment dates
start_time = datetime.datetime(2014, 4, 20, 0, 0, 0)
end_time = datetime.datetime(2015, 11, 22, 0, 0, 0)

rec = xr.open_dataset(recovered)
rec = rec.swap_dims({'obs':'time'})
tel = xr.open_dataset(telemetered)
tel = tel.swap_dims({'obs':'time'})

rec_slice = rec.sel(time=slice(start_time,end_time)) # select only deployment dates provided
tel_slice = tel.sel(time=slice(start_time,end_time))

global fName
head, tail = os.path.split(recovered)
fName = tail.split('.', 1)[0]
title = fName[0:27]
platform1 = title.split('-')[0]
platform2 = platform1 + '-' + title.split('-')[1]

# Index time by month and year (recovered and telemetered)
time_rec = rec_slice['time']
gMonth_rec = time_rec['time.month']
months_rec = np.unique(gMonth_rec.data)

time_r = time_rec.data
t0_r = time_r[0] # first timestamp
t1_r = time_r[-1] # last timestamp

dir1 = os.path.join(save_dir, platform1, platform2, title, 'timeseries_overlay_monthly_' + str(t0_r)[0:10] + '_to_' + str(t1_r)[0:10])
createDir(dir1)
dir2 = os.path.join(save_dir, platform1, platform2, title, 'timeseries_overlay_panel_monthly_' + str(t0_r)[0:10] + '_to_' + str(t1_r)[0:10])
createDir(dir2)

time_tel = tel_slice['time']
gMonth_tel = time_tel['time.month']
months_tel = np.unique(gMonth_tel.data)

time_t = time_tel.data


# Identifies variables to skip when plotting
misc_vars = ['quality', 'string', 'timestamp', 'deployment', 'id', 'provenance', 'qc',  'time', 'mission', 'obs',
            'volt', 'ref', 'sig', 'amp', 'rph', 'calphase', 'phase', 'therm']
reg_ex = re.compile('|'.join(misc_vars))

sci_vars_rec = [s for s in rec.variables if not reg_ex.search(s)]
sci_vars_tel = [s for s in tel.variables if not reg_ex.search(s)]

print 'Recovered months present in file: ' + str(months_rec)
print 'Telemetered months present in file: ' + str(months_tel)

# Only plots months contained in the recovered dataset, if there is additional telemetered data it won't be plotted
for x in months_rec: # index by month
    ind_month_rec = x == gMonth_rec.data
    temp_time_rec = time_r[ind_month_rec]

    ind_month_tel = x == gMonth_tel.data
    temp_time_tel = time_t[ind_month_tel]

    for r in sci_vars_rec:
        for t in sci_vars_tel:
            if r == t: # check if r and t are the same variable
                print r
                rN = rec_slice[r]
                rD = rN.data[ind_month_rec]

                tN = tel_slice[t]
                tD = tN.data[ind_month_tel]

                m = datetime.date(1900, x, 1).strftime('%B')
                year = str(pd.Timestamp(time_r[0]).year)

                plotArgs1 = (rN, title, m, year, str(x), dir1)
                plot_timeseries_overlay(temp_time_rec, temp_time_tel, rD, tD, plotArgs1)

                plotArgs2 = (rN, title, m, year, str(x), dir2)
                plot_timeseries_overlay_panel(temp_time_rec, temp_time_tel, rD, tD, plotArgs2)