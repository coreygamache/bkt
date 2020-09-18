from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from bkt.db import get_db
from scipy.optimize import curve_fit
import numpy as np
import requests
import json
import time

api_key = '82e9648595b617cdc3806a8868249a8a'

bp = Blueprint('kill_times', __name__)

def exponential(x, a, b):
    return a * np.exp(b * x)

@bp.route('/')
def index():

    # raid IDs
    raid_ids = {'mc':1000, 'bwl':1002, 'aq':1005}

    # raid boss IDs
    mc_boss_ids = {'lucifron':663, 'magmadar':664, 'gehennas':665, 'garr':666, 'geddon':667, 'shazzrah':668, 'sulfuron':669, 'golemagg':670, 'domo':671, 'ragnaros':672}
    bwl_boss_ids = {'razorgore':610, 'vael':611, 'broodlord':612, 'firemaw':613, 'ebonroc':614, 'flamegor':615, 'chromaggus':616, 'nefarian':617}
    aq_boss_ids = {'skeram':709, 'bug_trio':710, 'sartura':711, 'fankriss':712, 'viscidus':713, 'huhuran':714, 'twin_emps':715, 'ouro':716, 'cthun':717}

    # initialize fight lists
    mc_fights = {'lucifron':list(), 'magmadar':list(), 'gehennas':list(), 'garr':list(), 'geddon':list(), 'shazzrah':list(), 'sulfuron':list(), 'golemagg':list(), 'domo':list(), 'ragnaros':list()}
    bwl_fights = {'razorgore':list(), 'vael':list(), 'broodlord':list(), 'firemaw':list(), 'ebonroc':list(), 'flamegor':list(), 'chromaggus':list(), 'nefarian':list()}
    aq_fights = {'skeram':list(), 'bug_trio':list(), 'sartura':list(), 'fankriss':list(), 'viscidus':list(), 'huhuran':list(), 'twin_emps':list(), 'ouro':list(), 'cthun':list()}

    # get reports from API
    response = requests.get("https://classic.warcraftlogs.com/v1/reports/guild/Released/Pagle/US?api_key=82e9648595b617cdc3806a8868249a8a")
    reports = response.json()
    reports.reverse() # reports are ordered newest first so order must be reversed

    selected_raid = raid_ids['aq']

    for report in reports:

        # skip reports that aren't MC, BWL, or AQ40
        if report['zone'] != selected_raid:
            continue

        request_string = "https://classic.warcraftlogs.com/v1/report/fights/" + report['id'] + "?api_key=" + api_key
        response = requests.get(request_string)
        fights = response.json()

        for fight in fights['fights']:
            if fight['boss'] != 0 and fight['kill'] == True:
                if report['zone'] == raid_ids['mc']: # Molten Core
                    if fight['boss'] == mc_boss_ids['lucifron']:
                        mc_fights['lucifron'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == mc_boss_ids['magmadar']:
                        mc_fights['magmadar'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == mc_boss_ids['gehennas']:
                        mc_fights['gehennas'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == mc_boss_ids['garr']:
                        mc_fights['garr'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == mc_boss_ids['geddon']:
                        mc_fights['geddon'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == mc_boss_ids['shazzrah']:
                        mc_fights['shazzrah'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == mc_boss_ids['sulfuron']:
                        mc_fights['sulfuron'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == mc_boss_ids['golemagg']:
                        mc_fights['golemagg'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == mc_boss_ids['domo']:
                        mc_fights['domo'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == mc_boss_ids['ragnaros']:
                        mc_fights['ragnaros'].append(fight['end_time'] - fight['start_time'])
                elif report['zone'] == raid_ids['bwl']: # Blackwing Lair
                    if fight['boss'] == bwl_boss_ids['razorgore']:
                        bwl_fights['razorgore'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == bwl_boss_ids['vael']:
                        bwl_fights['vael'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == bwl_boss_ids['broodlord']:
                        bwl_fights['broodlord'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == bwl_boss_ids['firemaw']:
                        bwl_fights['firemaw'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == bwl_boss_ids['ebonroc']:
                        bwl_fights['ebonroc'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == bwl_boss_ids['flamegor']:
                        bwl_fights['flamegor'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == bwl_boss_ids['chromaggus']:
                        bwl_fights['chromaggus'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == bwl_boss_ids['nefarian']:
                        bwl_fights['nefarian'].append(fight['end_time'] - fight['start_time'])
                elif report['zone'] == raid_ids['aq']: # Temple of Ahn'Qiraj
                    if fight['boss'] == aq_boss_ids['skeram']:
                        aq_fights['skeram'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == aq_boss_ids['bug_trio']:
                        aq_fights['bug_trio'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == aq_boss_ids['sartura']:
                        aq_fights['sartura'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == aq_boss_ids['fankriss']:
                        aq_fights['fankriss'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == aq_boss_ids['viscidus']:
                        aq_fights['viscidus'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == aq_boss_ids['huhuran']:
                        aq_fights['huhuran'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == aq_boss_ids['twin_emps']:
                        aq_fights['twin_emps'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == aq_boss_ids['ouro']:
                        aq_fights['ouro'].append(fight['end_time'] - fight['start_time'])
                    elif fight['boss'] == aq_boss_ids['cthun']:
                        aq_fights['cthun'].append(fight['end_time'] - fight['start_time'])

    # predict next boss kill times
    if selected_raid == raid_ids['mc']:
        fights = mc_fights
    elif selected_raid == raid_ids['bwl']:
        fights = bwl_fights
    elif selected_raid == raid_ids['aq']:
        x_vals = np.linspace(1, len(aq_fights['cthun']), len(aq_fights['cthun']))
        pars, cov = pars, cov = curve_fit(exponential, x_vals, aq_fights['cthun'], [0, 0], bounds=(-np.inf, np.inf))
        kill_time = exponential(len(x_vals) + 1, *pars) / 1000.0
        data = {'boss':'C\'thun', 'kill_time':kill_time}

#    for report in reports:
#        s, ms = divmod(report['start'], 1000)
#        report['start'] = '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)
#        s, ms = divmod(report['end'], 1000)
#        report['end'] = '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)

    return render_template('kill_times/index.html', data = data)
