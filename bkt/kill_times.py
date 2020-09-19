from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
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

# decorator function (requires api key to be entered, otherwise redirects to options page)
def api_key_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user_api_key = session.get('api_key')
        if user_api_key is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def exponential(x, a, b):
    return a * np.exp(b * x)

def millis2string(millis):
    millis = int(millis)
    seconds = (millis / 1000) % 60
    seconds = str(int(seconds)) if seconds >= 10 else '0' + str(int(seconds))
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    time_string = str(minutes) + ':' + seconds
    return time_string

# takes list of fight dict objects
def predict_kill_time(fights):
    y_vals = list()
    y_vals_dmf = list()
    for fight in fights:
        if fight['dmf'] == False:
            y_vals.append(fight['end_time'] - fight['start_time'])
        else:
            y_vals_dmf.append(fight['end_time'] - fight['start_time'])
    x_vals = np.linspace(1, len(y_vals), len(y_vals))
    x_vals_dmf = np.linspace(1, len(y_vals_dmf), len(y_vals_dmf))

    print(x_vals)
    print(x_vals_dmf)
    print(y_vals)
    print(y_vals_dmf)

    # predict normal kill time
    if len(x_vals) > 1:
        pars, cov = curve_fit(exponential, x_vals, y_vals, [0, 0], bounds=(-np.inf, np.inf))
        kill_time = exponential(len(x_vals) + 1, *pars)
    elif len(x_vals) == 1:
        kill_time = y_vals[0]
    else:
        kill_time = 0
    kill_time = millis2string(kill_time)

    # predict Darkmoon Faire buff week kill time
    if len(x_vals_dmf) > 1:
        pars, cov = curve_fit(exponential, x_vals_dmf, y_vals_dmf, [0, 0], bounds=(-np.inf, np.inf))
        kill_time_dmf = exponential(len(x_vals_dmf) + 1, *pars)
    elif len(x_vals_dmf) == 1:
        kill_time_dmf = y_vals_dmf[0]
    else:
        kill_time_dmf = 0
    kill_time_dmf = millis2string(kill_time_dmf)

    data = {'name':fights[0]['name'], 'kill_time':kill_time, 'kill_time_dmf':kill_time_dmf}
    return data

# views

# set options view
@bp.route('/options', methods=('GET', 'POST'))
def options():
    if request.method == 'POST':
        user_api_key = request.form['api_key']
        raid_id = request.form['raid_id']

        if user_api_key is None:
            error = 'No API key entered.'

        if error is None:
            session.clear()
            session['api_key'] = user_api_key
            return redirect(url_for('index'))

    return render_template('options.html')

# index view
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

    selected_raid = raid_ids['bwl']

    for report in reports:

        # skip reports that aren't for selected raid
        if report['zone'] != selected_raid:
            continue

        # check report for Darkmoon Faire buffs
        request_string = "https://classic.warcraftlogs.com/v1/report/tables/buffs/" + report['id'] + "?start=0&end=999999999&abilityid=23768&api_key=" + api_key
        response = requests.get(request_string)
        buffs = response.json()
        dmf_buff = True if len(buffs['auras']) > 0 else False

        # get fights for current report
        request_string = "https://classic.warcraftlogs.com/v1/report/fights/" + report['id'] + "?start=0&end=999999999&abilityid=23768&api_key=" + api_key
        response = requests.get(request_string)
        fights = response.json()

        for fight in fights['fights']:
            if fight['boss'] != 0 and fight['kill'] == True:
                fight['dmf'] = dmf_buff # indicate whether fight happened on a Darkmoon Faire buff week
                if report['zone'] == raid_ids['mc']: # Molten Core
                    if fight['boss'] == mc_boss_ids['lucifron']:
                        mc_fights['lucifron'].append(fight)
                    elif fight['boss'] == mc_boss_ids['magmadar']:
                        mc_fights['magmadar'].append(fight)
                    elif fight['boss'] == mc_boss_ids['gehennas']:
                        mc_fights['gehennas'].append(fight)
                    elif fight['boss'] == mc_boss_ids['garr']:
                        mc_fights['garr'].append(fight)
                    elif fight['boss'] == mc_boss_ids['geddon']:
                        mc_fights['geddon'].append(fight)
                    elif fight['boss'] == mc_boss_ids['shazzrah']:
                        mc_fights['shazzrah'].append(fight)
                    elif fight['boss'] == mc_boss_ids['sulfuron']:
                        mc_fights['sulfuron'].append(fight)
                    elif fight['boss'] == mc_boss_ids['golemagg']:
                        mc_fights['golemagg'].append(fight)
                    elif fight['boss'] == mc_boss_ids['domo']:
                        mc_fights['domo'].append(fight)
                    elif fight['boss'] == mc_boss_ids['ragnaros']:
                        mc_fights['ragnaros'].append(fight)
                elif report['zone'] == raid_ids['bwl']: # Blackwing Lair
                    if fight['boss'] == bwl_boss_ids['razorgore']:
                        bwl_fights['razorgore'].append(fight)
                    elif fight['boss'] == bwl_boss_ids['vael']:
                        bwl_fights['vael'].append(fight)
                    elif fight['boss'] == bwl_boss_ids['broodlord']:
                        bwl_fights['broodlord'].append(fight)
                    elif fight['boss'] == bwl_boss_ids['firemaw']:
                        bwl_fights['firemaw'].append(fight)
                    elif fight['boss'] == bwl_boss_ids['ebonroc']:
                        bwl_fights['ebonroc'].append(fight)
                    elif fight['boss'] == bwl_boss_ids['flamegor']:
                        bwl_fights['flamegor'].append(fight)
                    elif fight['boss'] == bwl_boss_ids['chromaggus']:
                        bwl_fights['chromaggus'].append(fight)
                    elif fight['boss'] == bwl_boss_ids['nefarian']:
                        bwl_fights['nefarian'].append(fight)
                elif report['zone'] == raid_ids['aq']: # Temple of Ahn'Qiraj
                    if fight['boss'] == aq_boss_ids['skeram']:
                        aq_fights['skeram'].append(fight)
                    elif fight['boss'] == aq_boss_ids['bug_trio']:
                        aq_fights['bug_trio'].append(fight)
                    elif fight['boss'] == aq_boss_ids['sartura']:
                        aq_fights['sartura'].append(fight)
                    elif fight['boss'] == aq_boss_ids['fankriss']:
                        aq_fights['fankriss'].append(fight)
                    elif fight['boss'] == aq_boss_ids['viscidus']:
                        aq_fights['viscidus'].append(fight)
                    elif fight['boss'] == aq_boss_ids['huhuran']:
                        aq_fights['huhuran'].append(fight)
                    elif fight['boss'] == aq_boss_ids['twin_emps']:
                        aq_fights['twin_emps'].append(fight)
                    elif fight['boss'] == aq_boss_ids['ouro']:
                        aq_fights['ouro'].append(fight)
                    elif fight['boss'] == aq_boss_ids['cthun']:
                        aq_fights['cthun'].append(fight)

    # predict next boss kill times
    data = list()
    if selected_raid == raid_ids['mc']:
        data.append(predict_kill_time(bwl_fights['lucifron']))
        data.append(predict_kill_time(bwl_fights['magmadar']))
        data.append(predict_kill_time(bwl_fights['gehennas']))
        data.append(predict_kill_time(bwl_fights['garr']))
        data.append(predict_kill_time(bwl_fights['geddon']))
        data.append(predict_kill_time(bwl_fights['shazzrah']))
        data.append(predict_kill_time(bwl_fights['sulfuron']))
        data.append(predict_kill_time(bwl_fights['golemagg']))
        data.append(predict_kill_time(bwl_fights['domo']))
        data.append(predict_kill_time(bwl_fights['ragnaros']))
    elif selected_raid == raid_ids['bwl']:
        data.append(predict_kill_time(bwl_fights['razorgore']))
        data.append(predict_kill_time(bwl_fights['vael']))
        data.append(predict_kill_time(bwl_fights['broodlord']))
        data.append(predict_kill_time(bwl_fights['firemaw']))
        data.append(predict_kill_time(bwl_fights['ebonroc']))
        data.append(predict_kill_time(bwl_fights['flamegor']))
        data.append(predict_kill_time(bwl_fights['chromaggus']))
        data.append(predict_kill_time(bwl_fights['nefarian']))
    elif selected_raid == raid_ids['aq']:
        data.append(predict_kill_time(aq_fights['skeram']))
        data.append(predict_kill_time(aq_fights['bug_trio']))
        data.append(predict_kill_time(aq_fights['sartura']))
        data.append(predict_kill_time(aq_fights['fankriss']))
        data.append(predict_kill_time(aq_fights['viscidus']))
        data.append(predict_kill_time(aq_fights['huhuran']))
        data.append(predict_kill_time(aq_fights['twin_emps']))
        data.append(predict_kill_time(aq_fights['ouro']))
        data.append(predict_kill_time(aq_fights['cthun']))

#    for report in reports:
#        s, ms = divmod(report['start'], 1000)
#        report['start'] = '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)
#        s, ms = divmod(report['end'], 1000)
#        report['end'] = '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)

    return render_template('kill_times/index.html', data = data)
