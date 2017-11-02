#! /usr/local/bin/python

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re
import os
import matplotlib.cm as cm
import datetime

'''
This script is used to create profile plots from all netCDF files in a directory, by deployment.
Time is indicated by color.

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


def plot_profiles(t, yN, yD, y_units, xN, xD, x_units, plt_title, t0, t1, fName, dir):
    fig,ax = plt.subplots()
    plt.grid()
    plt.margins(y=.1, x=.1)
    minorLocator = ticker.AutoMinorLocator()

    colors = cm.rainbow(np.linspace(0,1, len(t)))
    ax.scatter(xD, yD, c = colors, edgecolor='None')
    
    # Image size
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 12
    fig_size[1] = 8.5
    plt.rcParams["figure.figsize"] = fig_size

    # setup axes
    ax.xaxis.set_minor_locator(minorLocator)
    xax = ax.get_xaxis().get_major_formatter()

    y_formatter = ticker.ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(y_formatter)
    plt.grid()
    plt.gca().invert_yaxis()

    ax.set_xlabel(xN + " (" + x_units + ")", fontsize=11) # x label
    ax.set_ylabel(yN + ' (' + y_units + ')', fontsize=11) # y label
    ax.set_title(plt_title + '\n' + str(t0)[0:19] + ' to ' + str(t1)[0:19], fontsize=12) # title
    filename = str(fName + '-' + xN + ".png")
    save_file = os.path.join(dir, filename)
    plt.savefig(save_file,dpi=100) # save figure
    plt.close()


def main(rootdir,saveDir):
    for root, dirs, files in os.walk(rootdir):
        for filename in files:
            if filename.endswith('.nc'):
                print filename
                file = os.path.join(root,filename)
                f = xr.open_dataset(file)
                f = f.swap_dims({'obs':'time'})
                #f_slice = f.sel(time=slice(stime,etime))

                fName = os.path.split(file)[-1].split('.')[0]
                platform = f.subsite
                title = platform + '-' + f.node + '-' + f.sensor + '-' + f.collection_method
                deployment = fName.split('_')[0]

                t = f['time'].data
                t0 = t[0] # first timestamp
                t1 = t[-1] # last timestamp
                dir = os.path.join(saveDir, 'profiles', deployment)
                createDir(dir)

                pressure_vars = ['sci_water_pressure_dbar', 'ctdgv_m_glider_instrument_recovered-sci_water_pressure_dbar',
                             'ctdgv_m_glider_instrument-sci_water_pressure_dbar','ctdpf_ckl_seawater_pressure']

                rePressure = re.compile('|'.join(pressure_vars))
                pressure = [s for s in f.variables if rePressure.search(s)]
                yN = ''.join(pressure)
                yD = f.variables[yN].data
                y_units = f[yN].units

                skipvars = ['quality', 'string', 'timestamp', 'deployment', 'id', 'provenance', 'qc',  'time', 'mission', 'obs',
                            'lat', 'lon', 'volt', 'ref', 'sig', 'amp', 'rph', 'calphase', 'phase', 'therm', 'pressure']

                reSkip = re.compile('|'.join(skipvars))
                varList = []
                for varNum in f.variables:
                    varList.append(str(varNum))

                xVars = [s for s in varList if not reSkip.search(s)]

                for xN in xVars:
                    print xN
                    xD = f.variables[xN].data
                    x_units = f[xN].units
                    plt_title = title + '_' + xN
                    plot_profiles(t, yN, yD, y_units, xN, xD, x_units, plt_title, t0, t1, fName, dir)


if __name__ == '__main__':
    rootdir = '/Users/lgarzio/Documents/OOI/DataReviews/2017/RIC2/GI02HYPM/GI02HYPM-WFP02-04-CTDPFL000/data'
    saveDir = '/Users/lgarzio/Documents/OOI/DataReviews/2017/RIC2/GI02HYPM/GI02HYPM-WFP02-04-CTDPFL000/plots'
    # stime = datetime.datetime(2013, 1, 1, 0, 0, 0)
    # etime = datetime.datetime(2017, 12, 30, 0, 0, 0)
    # main(rootdir,saveDir,stime,etime)
    main(rootdir,saveDir)