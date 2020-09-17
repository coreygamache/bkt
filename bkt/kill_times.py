from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from bkt.db import get_db
import requests
import json

bp = Blueprint('kill_times', __name__)

@bp.route('/')
def index():
    db = get_db()
    response = requests.get("https://classic.warcraftlogs.com/v1/reports/guild/Released/Pagle/US?api_key=82e9648595b617cdc3806a8868249a8a")
    reports = response.json()
    db.execute(
        'INSERT INTO'
    )
#    reports = db.execute(
#        'SELECT *'
#        ' FROM report'
#        ' ORDER BY start DESC'
#    ).fetchall()
    return render_template('kill_times/index.html', reports = reports)
