from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from bkt.db import get_db
import requests
import json
import datetime

bp = Blueprint('kill_times', __name__)

@bp.route('/')
def index():
    db = get_db()
    response = requests.get("https://classic.warcraftlogs.com/v1/reports/guild/Released/Pagle/US?api_key=82e9648595b617cdc3806a8868249a8a")
    reports = response.json()

    for report in reports:
        report['start'] = datetime.datetime.fromtimestamp(report['start']).strftime('%Y-%m-%d %H:%M:%S.%f')
        report['end'] = datetime.datetime.fromtimestamp(report['end']).strftime('%Y-%m-%d %H:%M:%S.%f')

    for report in reports:
        db.execute(
            'INSERT INTO report (wcl_id, title, owner, start, end, zone)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            (report['id'], report['title'], report['owner'], (strftime('%s',report['start'])), report['end'], report['zone'])
        )

    db.commit()
#    return redirect(url_for('kill_times.index'))

    reports = db.execute(
        'SELECT title, start'
        ' FROM report'
#        ' ORDER BY start DESC'
    ).fetchall()
    return render_template('kill_times/index.html', reports = reports)
