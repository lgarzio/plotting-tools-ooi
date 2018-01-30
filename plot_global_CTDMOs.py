"""
Created on Nov 16 2017

@author: lgarzio
@brief: This script is used to plot a timeseries of all CTDMO recovered_inst data from an entire platform by deployment
@usage:
rootdir: location of files
"""

import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import os
import numpy as np
import datetime
from collections import OrderedDict


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


def get_deployment(rootdir):
    dlist = []
    for root, dirs, files in os.walk(rootdir):
        for filename in files:
            if filename.endswith('.nc'):
                deployment = filename[0:14]
                if deployment not in dlist:
                    dlist.append(deployment)
        return dlist


def get_data(rootdir,v,deploy):
    dict = OrderedDict()
    for root, dirs, files in os.walk(rootdir):
        for filename in files:
            if filename.endswith('.nc'):
                deployment = filename[0:14]
                if deploy == deployment:
                    file = os.path.join(root,filename)
                    f = xr.open_dataset(file)
                    f = f.swap_dims({'obs':'time'})
                    refdes = f.subsite + '-' + f.node + '-' + f.sensor

                    f_slice = f.sel(time=slice(start_time,end_time)) # select only deployment dates provided

                    t = f_slice['time'].data

                    y = f_slice[v]

                    yD = y.data
                    yunits = y.units
                    dict[refdes] = {}
                    dict[refdes]['time'] = t
                    dict[refdes]['yD'] = yD
                    dict[refdes]['median'] = np.median(yD)
        return dict, yunits


rootdir = '/Users/lgarzio/Documents/OOI/'

# enter deployment dates
start_time = datetime.datetime(2013, 1, 1, 0, 0, 0)
end_time = datetime.datetime(2018, 2, 1, 0, 0, 0)

# Identifies variables to skip when plotting
plt_vars = ['ctdmo_seawater_pressure','ctdmo_seawater_temperature','ctdmo_seawater_conductivity','practical_salinity','density']

colors = ['red','firebrick','orange','gold','mediumseagreen','darkcyan','blue','darkgreen','purple','indigo','slategray','black']

for v in plt_vars:
    print v

    dlist = get_deployment(rootdir)

    for deploy in dlist:
        dict, yunits = get_data(rootdir,v,deploy)
        print 'Plotting %s' %deploy
        fig, ax1 = plt.subplots()

        refdes_list = []
        median_list = []
        #dlegend = {}
        for i, (key, value) in enumerate(dict.iteritems()):
            t = value['time']
            yD = value['yD']
            refdes = str(key)

            refdes_list.append(refdes)
            median_list.append(value['median'])

            #dlegend[str(refdes)] = colors[i]

            plt.plot(t, yD,c=colors[i],marker='.',markersize=.25)
            #ax.legend(['%s' %str(refdes)], loc='best', fontsize=8)

            if i == len(dict) - 1: # if the last dataset has been plotted
                plt.grid()
                plt.margins(y=.05, x=.05)

                # refdes on secondary y-axis only for pressure and density
                if v in ['ctdmo_seawater_pressure','density']:
                    ax2 = ax1.twinx()
                    ax2.set_ylim(ax1.get_ylim())
                    plt.yticks(median_list,refdes_list,fontsize=9)
                    plt.subplots_adjust(right=.73)

                # Format date axis
                df = mdates.DateFormatter('%Y-%m-%d')
                ax1.xaxis.set_major_formatter(df)
                fig.autofmt_xdate()

                # Format y-axis to disable offset
                y_formatter = ticker.ScalarFormatter(useOffset=False)
                ax1.yaxis.set_major_formatter(y_formatter)

                ax1.set_ylabel(v + " ("+ yunits + ")")
                ax1.set_title(refdes.split('-')[0] + ' ' + deploy)
                fname = deploy + '_' + refdes.split('-')[0] + '_' + v

                sdir = os.path.join(rootdir, 'timeseries')
                createDir(sdir)
                save_file = os.path.join(sdir, fname)  # create save file name
                plt.savefig(str(save_file),dpi=150) # save figure
                plt.close()
            else:
                continue