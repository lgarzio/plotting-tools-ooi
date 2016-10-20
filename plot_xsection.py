#! /usr/local/bin/python

import xarray as xr
import matplotlib.pyplot as plt
import re
import datetime
import matplotlib.dates as mdates
import os

'''
This script is used to create cross-section plots from netCDF or ncml files for a time range specified by the user.
Color bar limits are also set by the user.

'''

def plot_xsection(x, y, z, lim, args):
    # Close any existing plots
    plt.close('all')

    xD = x.data
    yD = y.data
    zD = z.data

    fig,ax = plt.subplots()
    plt.grid()
    plt.ylim([0,200])
    # ax = plt.gca()
    ax.invert_yaxis()
    # f, ax = plt.subplots(1, 1)

    # Image size
    # fig_size = plt.rcParams["figure.figsize"]
    # fig_size[0] = 12
    # fig_size[1] = 8.5
    # plt.rcParams["figure.figsize"] = fig_size

    # Format the date axis
    #plt.locator_params(nbins=4)
    df = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(df)
    fig.autofmt_xdate()

    # colors = cm.rainbow(np.linspace(0,1, len(z)))
    # c = cm.jet(z)
    sc = plt.scatter(xD, yD, s=2, c=zD, edgecolors='face')

    # add colorbar
    bar = fig.colorbar(sc, ax=ax, label=args[2] + " (" + args[3] + ")")
    bar
    bar.formatter.set_useOffset(False)
    plt.clim(lim)

    # plot labels
    plt.ylabel(args[0] + ' (' + args[1] + ')') # y label
    plt.xlabel("Time (GMT)")
    plt.title(args[6], fontsize = 12)

    save_dir = args[5]
    save_file = os.path.join(save_dir, args[4])
    plt.savefig(str(save_file), dpi=100) # save figure
    plt.close()


saveDir = '/Users/lgarzio/Documents/OOI/DataReviews/restinclass/Endurance/CE05MOAS/CE05MOAS-GL320/xsection_deployment1/'

#urls = ['http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/02-FLORTM000/recovered_host/CE05MOAS-GL319-02-FLORTM000-flort_m_glider_recovered-recovered_host/CE05MOAS-GL319-02-FLORTM000-flort_m_glider_recovered-recovered_host.ncml']
urls = ['http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/05-CTDGVM000/recovered_host/CE05MOAS-GL320-05-CTDGVM000-ctdgv_m_glider_instrument_recovered-recovered_host/CE05MOAS-GL320-05-CTDGVM000-ctdgv_m_glider_instrument_recovered-recovered_host.ncml',
        'http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/04-DOSTAM000/recovered_host/CE05MOAS-GL320-04-DOSTAM000-dosta_abcdjm_glider_recovered-recovered_host/CE05MOAS-GL320-04-DOSTAM000-dosta_abcdjm_glider_recovered-recovered_host.ncml',
        'http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/02-FLORTM000/recovered_host/CE05MOAS-GL320-02-FLORTM000-flort_m_glider_recovered-recovered_host/CE05MOAS-GL320-02-FLORTM000-flort_m_glider_recovered-recovered_host.ncml',
        'http://opendap.oceanobservatories.org/thredds/dodsC/rest-in-class/Coastal_Endurance/CE05MOAS/01-PARADM000/recovered_host/CE05MOAS-GL320-01-PARADM000-parad_m_glider_recovered-recovered_host/CE05MOAS-GL320-01-PARADM000-parad_m_glider_recovered-recovered_host.ncml']


start_time = datetime.datetime(2014, 10, 7, 0, 0, 0)
end_time = datetime.datetime(2014, 12, 29, 0, 0, 0)

datastrs = ['pressure','quality', 'string', 'timestamp', 'deployment', 'id', 'provenance', 'qc',  'time', 'mission', 'obs',
            'lat', 'lon', 'volt', 'ref', 'sig', 'amp', 'rph', 'calphase', 'phase']

reV = re.compile('|'.join(datastrs))

pressure_vars = ['sci_water_pressure_dbar', 'ctdgv_m_glider_instrument_recovered-sci_water_pressure_dbar',
                 'ctdgv_m_glider_instrument-sci_water_pressure_dbar']

rePressure = re.compile('|'.join(pressure_vars))

#define plotting limits
lim_den = [1022,1029]
lim_pracsal = [30,35]
lim_temp = [3,20]
lim_cond = [3,4.3]
lim_chl = [0,5]
lim_cdom = [0,10]
lim_bb = [0,0.006]
lim_DO2 = [0,300]
lim_DO1 = [0,360]
lim_DO_sat = [0,110]
lim_par = [0,3500]

for url in urls:
    print url
    f = xr.open_dataset(url)
    f = f.swap_dims({'obs':'time'})
    f_slice = f.sel(time=slice(start_time,end_time))
    fN = f_slice.source
    pressure = [s for s in f_slice.variables if rePressure.search(s)]
    pressure = ''.join(pressure)
    y = f_slice.variables[pressure]
    yN = pressure
    y_units = f[yN].units
    x = f_slice.variables['time']

    varList = []
    for varNum in f_slice.variables:
        varList.append(str(varNum))

    zVars = [s for s in varList if not reV.search(s)]

    for zN in zVars:
        z = f_slice.variables[zN]
        z_units = f[zN].units
        if zN == 'sci_seawater_density':
            lim = lim_den
        elif zN == 'sci_water_pracsal':
            lim = lim_pracsal
        elif zN == 'sci_water_temp':
            lim = lim_temp
        elif zN == 'sci_water_cond':
            lim = lim_cond
        elif zN == 'sci_flbbcd_chlor_units':
            lim = lim_chl
        elif zN == 'sci_flbbcd_cdom_units':
            lim = lim_cdom
        elif zN == 'sci_flbbcd_bb_units':
            lim = lim_bb
        elif zN == 'sci_abs_oxygen':
            lim = lim_DO2
        elif zN == 'sci_oxy4_oxygen':
            lim = lim_DO1
        elif zN == 'sci_oxy4_saturation':
            lim = lim_DO_sat
        elif zN == 'parad_m_par':
            lim = lim_par
        else:
            lim = float('NaN')

        title = fN.split('-')[0] + '-' + fN.split('-')[1] + '-' + fN.split('-')[2] + '-' + fN.split('-')[3] + '-' + fN.split('-')[4]
        fName = title + '_xsection_' + zN
        plotArgs = (yN, y_units, zN, z_units, fName, saveDir, title)
        plot_xsection(x, y, z, lim, plotArgs)
