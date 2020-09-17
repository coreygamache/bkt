    for report in reports:
        db.execute(
            'INSERT INTO report (wcl_id, title, owner, start, end, zone)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            (report['id'], report['title'], report['owner'], report['start'], report['end'], report['zone'])
        )

    db.commit()
    # return redirect(url_for('kill_times.index'))

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

                db.execute(
                    'INSERT INTO fight (wcl_id, start_time, end_time, boss, name)'
                    ' VALUES (?, ?, ?, ?, ?, ?)',
                    (report['id'], fight['start_time'], fight['end_time'], fight['boss'], fight['name'])
                )
