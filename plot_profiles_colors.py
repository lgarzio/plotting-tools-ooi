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
This script is used to create profile plots from netCDF or ncml files for a time range specified by the user.
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

def plot_profiles(x, y, t, args):
    xD = x.data
    yD = y.data

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

    ax.set_xlabel(args[0] + " (" + args[2] + ")", fontsize=11) # x label
    ax.set_ylabel(args[1] + ' (' + args[3] + ')', fontsize=11) # y label
    ax.set_title(args[4] + '\n' + args[5] + ' to ' + args[6], fontsize=12) # title
    filename = str(args[7]) + '_' + args[0] + ".png"
    save_file = os.path.join(args[8], filename)
    plt.savefig(save_file,dpi=100) # save figure
    plt.close()


save_dir = '/Users/lgarzio/Documents/OOI/DataReviews/restinclass/Endurance'

urls = ['http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/05-CTDGVM000/recovered_host/CE05MOAS-GL320-05-CTDGVM000-ctdgv_m_glider_instrument_recovered-recovered_host/CE05MOAS-GL320-05-CTDGVM000-ctdgv_m_glider_instrument_recovered-recovered_host.ncml',
        'http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/05-CTDGVM000/telemetered/CE05MOAS-GL320-05-CTDGVM000-ctdgv_m_glider_instrument-telemetered/CE05MOAS-GL320-05-CTDGVM000-ctdgv_m_glider_instrument-telemetered.ncml',
        'http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/02-FLORTM000/recovered_host/CE05MOAS-GL320-02-FLORTM000-flort_m_glider_recovered-recovered_host/CE05MOAS-GL320-02-FLORTM000-flort_m_glider_recovered-recovered_host.ncml',
        'http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/02-FLORTM000/telemetered/CE05MOAS-GL320-02-FLORTM000-flort_m_glider_instrument-telemetered/CE05MOAS-GL320-02-FLORTM000-flort_m_glider_instrument-telemetered.ncml',
        'http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/04-DOSTAM000/recovered_host/CE05MOAS-GL320-04-DOSTAM000-dosta_abcdjm_glider_recovered-recovered_host/CE05MOAS-GL320-04-DOSTAM000-dosta_abcdjm_glider_recovered-recovered_host.ncml',
        'http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/04-DOSTAM000/telemetered/CE05MOAS-GL320-04-DOSTAM000-dosta_abcdjm_glider_instrument-telemetered/CE05MOAS-GL320-04-DOSTAM000-dosta_abcdjm_glider_instrument-telemetered.ncml']

#urls = ['http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/04-DOSTAM000/recovered_host/CE05MOAS-GL320-04-DOSTAM000-dosta_abcdjm_glider_recovered-recovered_host/CE05MOAS-GL320-04-DOSTAM000-dosta_abcdjm_glider_recovered-recovered_host.ncml']

start_time = datetime.datetime(2014, 10, 7, 0, 0, 0)
end_time = datetime.datetime(2014, 12, 30, 0, 0, 0)


datastrs = ['quality', 'string', 'timestamp', 'deployment', 'id', 'provenance', 'qc',  'time', 'mission', 'obs',
            'lat', 'lon', 'volt', 'ref', 'sig', 'amp', 'rph', 'calphase', 'phase', 'therm']

reV = re.compile('|'.join(datastrs))

pressure_vars = ['sci_water_pressure_dbar', 'ctdgv_m_glider_instrument_recovered-sci_water_pressure_dbar',
                 'ctdgv_m_glider_instrument-sci_water_pressure_dbar']

rePressure = re.compile('|'.join(pressure_vars))

for url in urls:
    print url
    f = xr.open_dataset(url)
    f = f.swap_dims({'obs':'time'})
    f_slice = f.sel(time=slice(start_time,end_time))
#    fN = f_slice.source

    global fName
    head, tail = os.path.split(url)
    fName = tail.split('.', 1)[0]
    title = fName[0:27]
    platform1 = title.split('-')[0]
    platform2 = platform1 + '-' + title.split('-')[1]
    method = fName.split('-')[-1]

    t = f_slice['time'].data
    t0 = t[0] # first timestamp
    t1 = t[-1] # last timestamp
    dir1 = os.path.join(save_dir, platform1, platform2, title, method, 'profiles_' + str(t0)[0:10] + '_to_' + str(t1)[0:10])
    createDir(dir1)

    pressure = [s for s in f_slice.variables if rePressure.search(s)]
    pressure = ''.join(pressure)
    y = f_slice.variables[pressure]
    yN = pressure
    y_units = f[yN].units
    t = f_slice.variables['time']
    
    varList = []
    for varNum in f_slice.variables:
        varList.append(str(varNum))

    xVars = [s for s in varList if not reV.search(s)]

    for xN in xVars:
        print xN
        x = f_slice[xN]
        xD = x.data
        x_units = x.units
        plotArgs = (xN, yN, x_units, y_units, title, str(t0)[0:19], str(t1)[0:19], fName, dir1)
        plot_profiles(x, y, t, plotArgs)