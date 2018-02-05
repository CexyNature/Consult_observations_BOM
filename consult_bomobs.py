#!/usr/bin/env python
""""
Plot temperature, atmospheric pressure, wind speed and direction, and rainfall data from Weather Observation Stations
in North Tropical Coast and Tableblands, and Herbert and Lower Burdekin districts, Bureau of Meteorology.
For more information visit http://www.bom.gov.au/qld/observations/map.shtml
"""

import urllib.request
import json
import pandas as pd
from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import numpy as np
import math


__author__ = 'Cesar Herrera'
__copyright__ = 'Copyright (C) 2017 Cesar Herrera'
__license__ = 'GPL'

ap = argparse.ArgumentParser()
ap.add_argument('-s', '--station', required=True, help='Name of the station being query')
args = vars(ap.parse_args())

current_time = datetime.now().strftime('%Y%m%d%H%M%S')
time_fig = datetime.now().strftime('%d %B %Y, %H:%M')

locations = {'Townsville': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.94294.json',
             'Lucinda': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.94295.json',
             'Ingham': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.95291.json',
             'Cardwell': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.94292.json',
             'CapeFerguson': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.94297.json',
             'MtStuart': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.94272.json',
             'Alva': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.95296.json',
             'Ayr': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.95295.json',
             'Cairns': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.94287.json',
             'CowleyBeach': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.99218.json',
             'SouthJohnstone': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.95292.json',
             'Innisfail': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.94280.json',
             'Mareeba': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.95286.json',
             'CairnsRacecourse': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.94288.json',
             'ArlingtonReef': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.94284.json',
             'FanningRiver': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.94273.json',
             'Woolshed': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.95293.json',
             'TownsvilleAWR-Defence': 'http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.94271.json'}

target_url = locations.get(args['station'], None)


def main():
    with urllib.request.urlopen(target_url) as url:
        data_json = json.loads(url.read().decode())

        data = pd.DataFrame(data_json['observations']['data'])
        data = data.replace('-', np.nan)
        # print(data)
        data = data.where(data.notnull(), np.nan)
        # print(data)
        date_axis = data['local_date_time_full'].astype(str)
        # print(date_axis.dtype)
        date_axis = [datetime.strptime(obs, '%Y%m%d%H%M%S') for obs in date_axis]
        # print(date_axis)

        # date_axis_f = mdate.date2num(date_axis)
        hfmt = mdate.DateFormatter('%d%b\n%H:%M')

        fig = plt.figure(figsize=(12, 10))
        fig.suptitle(args['station'] + ' weather observations \nData from station '
                     + target_url[-10:-5] + ' Bureau of Meteorology' + '\n Figure printed at ' + time_fig)

        if data['air_temp'].isnull().all():
            ax = fig.add_subplot(2, 2, 1)
            ax.text(0.18, 0.65, 'There is not Temperature data \nfor this weather station',
                    style='oblique', bbox={'Facecolor': 'blue', 'alpha': 0.5, 'pad': 10})
            pass

        else:
            ax = fig.add_subplot(2, 2, 1)
            ax.patch.set_facecolor('lightgrey')
            ax.xaxis.set_major_formatter(hfmt)
            # ax.set_title('Temperature')
            # ax.set_xlabel('Time', fontsize=14)
            ax.xaxis.set_tick_params(labelsize=8)
            ax.set_ylabel('Air Temperature [°C]', fontsize=14)
            # plt.setp(ax.get_xticklabels(), size=8)
            ax.plot(date_axis, data['air_temp'], label='Air temperature')
            ax.plot(date_axis, data['apparent_t'], label='Apparent temperature')
            ax.legend(loc='upper left', shadow=True)
            # ax.scatter(date_axis, data['air_temp'])
            plt.grid()

        if data['press'].isnull().all():
            ax1 = fig.add_subplot(2, 2, 2)
            ax1.text(0.18, 0.65, 'There is not Atmospheric pressure data \nfor this weather station',
                     style='oblique', bbox={'Facecolor': 'blue', 'alpha': 0.5, 'pad': 10})
            pass

        # elif data['press'].isnan().all() is True:
        #     print('Yes')
        #     pass

        else:
            ax1 = fig.add_subplot(2, 2, 2)
            ax1.patch.set_facecolor('lightgrey')
            ax1.xaxis.set_major_formatter(hfmt)
            # ax1.set_title('Atmospheric pressure')
            # ax1.set_xlabel('Time', fontsize=14)
            ax1.xaxis.set_tick_params(labelsize=8)
            ax1.set_ylabel('Atmospheric pressure [hPa]', fontsize=14)
            ax1.plot(date_axis, data['press'])
            plt.grid()
            pass

        if data['wind_spd_kt'].isnull().all():
            ax2 = fig.add_subplot(2, 2, 3)
            ax2.text(0.18, 0.65, 'There is not Wind data \nfor this weather station',
                     style='oblique', bbox={'Facecolor': 'blue', 'alpha': 0.5, 'pad': 10})
            pass

        else:
            # data['wind_dir'] = data['wind_dir'].fillna(method='ffill')
            winds_dir = {
                'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5, 'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
                'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5, 'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5,
                'CALM': 0}

            # wind_angles = np.array([winds_dir[i] for i in data['wind_dir']])
            wind_angles = data['wind_dir'].map(winds_dir)
            # print(wind_angles)
            # print(wind_angles[-4:])
            # print(data['wind_spd_kt'].tail(4))
            # print(data['wind_dir'].tail(4))
            ax2 = fig.add_subplot(2, 2, 3, polar=True)
            # pi_half = np.pi/180.
            # ticks = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5]
            # ax2.set_xticks([pi_half * elem for elem in ticks])
            ax2.set_xticks(np.pi/180. * np.linspace(0, 360, 16, endpoint=False))
            ax2.annotate('North', xy=(1, 1), xycoords='data', xytext=(0.45, 1.1), textcoords="axes fraction")
            ax2.annotate('South', xy=(1, 1), xycoords='data', xytext=(0.45, -0.15), textcoords="axes fraction")
            ax2.set_theta_zero_location('N')
            ax2.set_theta_direction(-1)
            # ax2.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))
            ax2.set_ylim(0, 30)
            ax2.set_yticks(np.arange(0, 30, 6))
            ax2.bar(wind_angles[0:13] * np.pi/180, data['wind_spd_kt'].head(13))
            a = date_axis[0]
            b = date_axis[12]
            c = b - a
            # print(c.total_seconds()/3600)
            ax2.set_ylabel('Wind speed [knots] and direction\nin the last ' + str(c.total_seconds()/3600)
                           + ' hours', fontsize=14)
            ax2.yaxis.labelpad = 45

        if data['rain_trace'].isnull().all():
            ax3 = fig.add_subplot(2, 2, 4)
            ax3.text(0.18, 0.65, 'There is not Rainfall data \nfor this weather station',
                     style='oblique', bbox={'Facecolor': 'blue', 'alpha': 0.5, 'pad': 10})
            pass

        else:
            rainfall = pd.concat([data['local_date_time_full'].astype(str), data['rain_trace']], axis=1)
            rainfall['local_date_time_full'] = pd.to_datetime(rainfall['local_date_time_full'])
            rainfall['Time'] = rainfall['local_date_time_full'].dt.time
            reset_time = datetime.strptime('09:30:00', '%H:%M:%S')

            rain_data = rainfall['rain_trace']
            rain = []
            for value_i, value_i_plus_1, t, dt in zip(rain_data, rain_data[1:], rainfall['Time'],
                                                      rainfall['local_date_time_full']):
                if reset_time.time() != t:
                    if math.isnan(float(value_i)):
                        rain.append([str(dt), value_i])

                    else:
                        rain.append([str(dt), round(float(value_i) - float(value_i_plus_1), 1)])
                else:
                    rain.append([str(dt), float(value_i)])

            rain_1 = pd.DataFrame(np.array(rain), columns=['Date_time', 'Actual_rain'])
            rain_1['Date_time'] = pd.to_datetime(rain_1['Date_time'])
            rain_1['Date'] = rain_1['Date_time'].dt.date
            rain_1['Time'] = rain_1['Date_time'].dt.time
            rain_1['Day'] = rain_1['Date_time'].dt.weekday

            rain_1['Actual_rain'] = rain_1['Actual_rain'].astype(float)
            # print(len(rain_1))
            rain_1 = rain_1[pd.notnull(rain_1['Actual_rain'])]
            # print(len(rain_1))
            # print(rain_1)

            date_axis1 = rain_1['Date_time'].astype(str)
            # print(date_axis1)
            date_axis1 = [datetime.strptime(obs, '%Y-%m-%d %H:%M:%S') for obs in date_axis1]
            # print(date_axis)

            ax3 = fig.add_subplot(2, 2, 4)
            ax3.patch.set_facecolor('lightgrey')
            ax3.xaxis.set_major_formatter(hfmt)
            # ax3.set_title('Rain')
            ax3.set_xlabel('Date and Time', fontsize=14)
            ax3.xaxis.set_tick_params(labelsize=8)
            ax3.set_ylabel('Rain [mm]', fontsize=14)
            # ax3.set_ylim(0, 10)
            # ax3.set_yticks(np.arange(0, 10, 1))
            ax3.bar(date_axis1, rain_1['Actual_rain'])
            plt.grid()

        plt.tight_layout(pad=4, rect=[0, 0, 0.95, 0.95])
        plt.show()
        # plt.savefig('Summary_observations.png')

main()
