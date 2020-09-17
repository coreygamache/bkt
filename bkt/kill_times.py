from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from bkt.db import get_db
import requests
import json
import time

api_key = '82e9648595b617cdc3806a8868249a8a'

bp = Blueprint('kill_times', __name__)

@bp.route('/')
def index():
    db = get_db()

    # get reports from API
    response = requests.get("https://classic.warcraftlogs.com/v1/reports/guild/Released/Pagle/US?api_key=82e9648595b617cdc3806a8868249a8a")
    reports = response.json()
    # reports.reverse() # reports are ordered newest first so order must be reversed

    mc_boss_ids = {'lucifron':663, 'magmadar':664, 'gehennas':665, 'garr':666, 'geddon':667, 'shazzrah':668, 'sulfuron':669, 'golemagg':670, 'domo':671, 'ragnaros':672}
    bwl_boss_ids = {'razorgore':610, 'vael':611, 'broodlord':612, 'firemaw':613, 'ebonroc':614, 'flamegor':615, 'chromaggus':616, 'nefarian':617}
    aq_boss_ids = aq_fights = {'skeram':709, 'bug_trio':710, 'sartura':711, 'fankriss':712, 'viscidus':713, 'huhuran':714, 'twin_emps':715, 'ouro':716, 'cthun':717}

    mc_fights = {'lucifron':list(), 'magmadar':list(), 'gehennas':list(), 'garr':list(), 'geddon':list(), 'shazzrah':list(), 'sulfuron':list(), 'golemagg':list(), 'domo':list(), 'ragnaros':list()}
    bwl_fights = {'razorgore':list(), 'vael':list(), 'broodlord':list(), 'firemaw':list(), 'ebonroc':list(), 'flamegor':list(), 'chromaggus':list(), 'nefarian':list()}
    aq_fights = {'skeram':list(), 'bug_trio':list(), 'sartura':list(), 'fankriss':list(), 'viscidus':list(), 'huhuran':list(), 'twin_emps':list(), 'ouro':list(), 'cthun':list()}

    for report in reports:
        request_string = "https://classic.warcraftlogs.com/v1/report/fights/" + report['id'] + "?api_key=" + api_key
        response = requests.get(request_string)
        fights = response.json()

        for fight in fights['fights']:
            if fight['boss'] != 0 and fight['kill'] == 'true':
                if report['zone'] == 1000: # Molten Core
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
                elif report['zone'] == 1002: # Blackwing Lair
                    print('bwl')
                elif report['zone'] == 1005: # Temple of Ahn'Qiraj
                    print('aq')
        break

#    for report in reports:
#        s, ms = divmod(report['start'], 1000)
#        report['start'] = '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)
#        s, ms = divmod(report['end'], 1000)
#        report['end'] = '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)

    return render_template('kill_times/index.html', fights = mc_fights)
