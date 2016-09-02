#! /usr/local/bin/python

"""
Created on Mon Aug 22 2016

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

'''
This script is used to create timeseries plots of telemetered and recovered data from netCDF or ncml files, for a
user-specified timerange.
"Overlay" plots plot telemetered and recovered data on top of each other, and provide min and max values.
"Panel" plots create 3 plots on one page
    1. The top plot is a re-created overlay plot
    2. The middle plot is recovered data only
    3. The bottom plot is telemetered data only
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

def plot_timeseries_overlay(time_r, time_t, rN, tN, args):
    rD = rN.data
    tD = tN.data

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
    ax.set_ylabel(rN.name + " ("+ rN.units + ")")
    title = args[4] + '\n' + str(args[6]) + " to " + str(args[7])
    ax.set_title(title, fontsize=10)

    # Format legend
    rec_leg = mlines.Line2D([], [], markerfacecolor='none', marker='o', markeredgecolor='r', color='r',
                            label=("Recovered" + "\n  Max: %f" % args[0] + "\n  Min: %f" % args[1]))
    rec_tel = mlines.Line2D([], [], marker='x', markeredgecolor='b', ls=':',
                            label=("Telemetered" + "\n  Max: %f" % args[2] + "\n  Min: %f" % args[3]))
    ax.legend(handles=[rec_leg, rec_tel],loc='best', fontsize=8)

    # Save plot
    filename = args[4] + "_" + rN.name + "_overlay"
    save_file = os.path.join(args[5], filename)  # create save file name
    plt.savefig(str(save_file),dpi=150) # save figure
    plt.close()


def plot_timeseries_overlay_panel(time_r, time_t, rN, tN, args):
    rD = rN.data
    tD = tN.data

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
    ax2.set_ylabel(rN.name + " ("+ rN.units + ")")
    title = args[0] + '\n' + str(args[2]) + " to " + str(args[3])
    ax1.set_title(title, fontsize=10)

    # Legends
    ax1.legend(loc='best', fontsize=6, markerscale=.5)
    ax2.legend(loc='best', fontsize=6, markerscale=.5)
    ax3.legend(loc='best', fontsize=6, markerscale=.5)

    # Save plot
    filename = args[0] + "_" + rN.name + "_panel"
    save_file = os.path.join(args[1], filename)  # create save file name
    plt.savefig(str(save_file),dpi=150) # save figure
    plt.close()


save_dir = '/Users/lgarzio/Documents/OOI/DataReviews/restinclass/Endurance'

recovered = 'http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/05-CTDGVM000/recovered_host/CE05MOAS-GL319-05-CTDGVM000-ctdgv_m_glider_instrument_recovered-recovered_host/CE05MOAS-GL319-05-CTDGVM000-ctdgv_m_glider_instrument_recovered-recovered_host.ncml'
telemetered = 'http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/05-CTDGVM000/telemetered/CE05MOAS-GL319-05-CTDGVM000-ctdgv_m_glider_instrument-telemetered/CE05MOAS-GL319-05-CTDGVM000-ctdgv_m_glider_instrument-telemetered.ncml'

# enter deployment dates
start_time = datetime.datetime(2014, 04, 01, 0, 0, 0)
end_time = datetime.datetime(2014, 05, 29, 0, 0, 0)


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

time_r = rec_slice['time'].data
t0_r = time_r[0] # first timestamp
t1_r = time_r[-1] # last timestamp
dir1 = os.path.join(save_dir, platform1, platform2, title, 'timeseries_overlay_' + str(t0_r)[0:10] + '_to_' + str(t1_r)[0:10])
createDir(dir1)

dir2 = os.path.join(save_dir, platform1, platform2, title, 'timeseries_overlay_panel_' + str(t0_r)[0:10] + '_to_' + str(t1_r)[0:10])
createDir(dir2)

time_t = tel_slice['time'].data


# Identifies variables to skip when plotting
misc_vars = ['quality', 'string', 'timestamp', 'deployment', 'id', 'provenance', 'qc',  'time', 'mission', 'obs',
            'volt', 'ref', 'sig', 'amp', 'rph', 'calphase', 'phase', 'therm']
reg_ex = re.compile('|'.join(misc_vars))

sci_vars_rec = [s for s in rec.variables if not reg_ex.search(s)]
sci_vars_tel = [s for s in tel.variables if not reg_ex.search(s)]

for r in sci_vars_rec:
    for t in sci_vars_tel:
        if r == t: # check if r and t are the same variable
            print r
            rN = rec_slice[r]
            rD = rN.data

            tN = tel_slice[t]
            tD = tN.data

            # get min and max for recovered data
            try:
                rmin = np.nanmin(rD)
            except TypeError:
                rmin = ""
                continue

            try:
                rmax = np.nanmax(rD)
            except TypeError:
                rmax = ""
                continue

            # get min and max for telemetered data
            try:
                tmin = np.nanmin(tD)
            except TypeError:
                tmin = ""
                continue

            try:
                tmax = np.nanmax(tD)
            except TypeError:
                tmax = ""
                continue

            plotArgs1 = (rmax, rmin, tmax, tmin, title, dir1, t0_r, t1_r)
            plot_timeseries_overlay(time_r, time_t, rN, tN, plotArgs1)

            plotArgs2 = (title, dir2, t0_r, t1_r)
            plot_timeseries_overlay_panel(time_r, time_t, rN, tN, plotArgs2)