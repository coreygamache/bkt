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

    aq_reports = list()
    aq_fights = list()

    for report in reports:
        if report['zone'] == 1005:
            aq_reports.append(report)

    for report in aq_reports:
        request_string = "https://classic.warcraftlogs.com/v1/report/fights/" + report['id'] + "?api_key=" + api_key
        response = requests.get(request_string)
        fights = response.json()
        print(fights)

        for fight in fights['fights']:
            if fight['boss'] != 0 and fight['kill'] == "true":
                aq_fights.append(fight)


#    for report in reports:
#        s, ms = divmod(report['start'], 1000)
#        report['start'] = '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)
#        s, ms = divmod(report['end'], 1000)
#        report['end'] = '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)

    return render_template('kill_times/index.html', reports = aq_reports)
