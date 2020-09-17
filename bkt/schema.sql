DROP TABLE IF EXISTS report;
DROP TABLE IF EXISTS parse;

CREATE TABLE report (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  wcl_id TEXT NOT NULL,
  title TEXT NOT NULL,
  owner TEXT NOT NULL,
  start FROM_UNIXTIME(ms * 0.001) NOT NULL,
  end FROM_UNIXTIME(ms * 0.001) NOT NULL,
  zone INTEGER NOT NULL
);

CREATE TABLE parse (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  wcl_id INTEGER NOT NULL,
  start_time TIMESTAMP(3) NOT NULL,
  end_time TIMESTAMP(3) NOT NULL,
  boss TEXT NOT NULL,
  name TEXT NOT NULL,
  kill BOOLEAN
);
