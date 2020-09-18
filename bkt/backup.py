    db = get_db()

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







INDEX

{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Boss Kill Times{% endblock %}</h1>
{% endblock %}

{% block content %}
  {% for report in reports %}
    <article class="">
      <header>
        <div>
          <h1>{{ report['title'] }}</h1>
        </div>
      </header>
      <p class="body">report id: {{ report['id'] }}</p>
      <p class="body">report date: {{ report['start'] }}</p>
    </article>
    {% if not loop.last %}
      <hr>
    {% endif %}
  {% endfor %}
{% endblock %}
