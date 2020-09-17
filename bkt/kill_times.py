from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from bkt.db import get_db
import requests
import json
import time

bp = Blueprint('kill_times', __name__)

@bp.route('/')
def index():
    db = get_db()

    # get reports from API
#    response = requests.get("https://classic.warcraftlogs.com/v1/reports/guild/Released/Pagle/US?api_key=82e9648595b617cdc3806a8868249a8a")
#    reports = response.json()

#    for report in reports:
#        db.execute(
#            'INSERT INTO report (wcl_id, title, owner, start, end, zone)'
#            ' VALUES (?, ?, ?, ?, ?, ?)',
#            (report['id'], report['title'], report['owner'], report['start'], report['end'], report['zone'])
#        )

#    db.commit()
#    return redirect(url_for('kill_times.index'))

    reports = db.execute(
        'SELECT wcl_id AS id, title, datetime(start / 1000, \'unixepoch\', \'localtime\') AS start'
        ' FROM report'
        ' ORDER BY start DESC'
    ).fetchall()

    aq_reports = db.execute(
        'SELECT wcl_id as id, title, datetime(start / 1000, \'unixepoch\', \'localtime\') AS start, zone'
        ' FROM report'
        ' WHERE zone = 1005'
        ' ORDER BY start DESC'
    ).fetchall()

#    for report in reports:
#        s, ms = divmod(report['start'], 1000)
#        report['start'] = '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)
#        s, ms = divmod(report['end'], 1000)
#        report['end'] = '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)

    return render_template('kill_times/index.html', reports = aq_reports)
