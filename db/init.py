#!/usr/bin/env python3

import sqlite3 as sq

db = sq.connect('./db/database')
cur = db.cursor()
with open('db/create.sql') as f:
    cur.executescript(f.read())
