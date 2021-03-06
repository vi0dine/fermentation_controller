import datetime
import sqlite3
from sqlite3 import Error, Row

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = dict_factory
        init_tables(conn)
    except Error as e:
        print(e)
    
    return conn

def init_tables(conn):
    try:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS batches (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                name text NOT NULL,
                                current integer DEFAULT 0,
                                created_at integer DEFAULT (strftime('%s','now'))
                            ); """)
        c.execute("""CREATE TABLE IF NOT EXISTS fermentation_steps (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                current integer DEFAULT 0,
                                temperature real NOT NULL,
                                begin_date integer NOT NULL,
                                end_date integer NOT NULL,
                                batch_id integer NOT NULL,
                                created_at integer DEFAULT (strftime('%s','now')),
                                FOREIGN KEY (batch_id) REFERENCES batches (id)
                            );""")
        c.execute("""CREATE TABLE IF NOT EXISTS batch_temperature_readings (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                temperature real NOT NULL,
                                time integer DEFAULT (strftime('%s','now')),
                                batch_id integer NOT NULL,
                                fermentation_step_id integer NOT NULL,
                                FOREIGN KEY (fermentation_step_id) REFERENCES fermentation_steps (id),
                                FOREIGN KEY (batch_id) REFERENCES batches (id)
                            ); """)
    except Error as e:
        print(e)

def get_batches(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM batches")

    rows = cur.fetchall()
    return rows

def get_current_batch(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM batches WHERE current = 1 ORDER BY created_at DESC")

    rows = cur.fetchone()
    return rows

def create_batch(conn, batch):
    sql = ''' INSERT INTO batches(name)
            VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (batch,))
    conn.commit()
    return cur.lastrowid

def update_batch(conn, batch):
    cur = conn.cursor()
    if batch["current"] == 1:
        cur.execute("""UPDATE batches SET current = 0""")

    cur.execute("""UPDATE batches SET name = ?, current = ? WHERE id = ?""", (batch["name"], batch["current"], batch["id"]))
    conn.commit()
    
    return cur.lastrowid

def get_steps(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM batches WHERE current = 1")

    current_batch = cur.fetchone()

    if current_batch:
        cur.execute("SELECT * FROM fermentation_steps WHERE batch_id = ? ORDER BY begin_date ASC", (current_batch["id"],))
        rows = cur.fetchall()
        return rows

def get_current_step(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM fermentation_steps WHERE current = 1 ORDER BY created_at DESC")

    rows = cur.fetchone()
    return rows

def create_step(conn, step):
    sql = ''' INSERT INTO fermentation_steps(temperature, begin_date, end_date, batch_id)
            VALUES(?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, step)
    conn.commit()
    return cur.lastrowid

def update_step(conn, step):
    cur = conn.cursor()
    if step["current"]:
        cur.execute("UPDATE fermentation_steps SET current = 0")

    cur.execute("""UPDATE fermentation_steps SET temperature = ?, 
                                                 current = ?,
                                                 begin_date = ?,
                                                 end_date = ? WHERE id = ?""", 
                                                 (step["temperature"], step["current"], step["begin_date"], step["end_date"], step["id"]))
    conn.commit()
    return cur.lastrowid

def get_readings(conn, params):
    cur = conn.cursor()
    cur.execute("SELECT * FROM batches WHERE current = 1")
    current_batch = cur.fetchone()

    if current_batch:
        cur.execute("""SELECT r.temperature, r.time, f.temperature AS desired
                       FROM batch_temperature_readings AS r
                       LEFT JOIN fermentation_steps AS f
                       ON r.fermentation_step_id = f.id
                       WHERE r.batch_id = ? AND r.time > ?
                       ORDER BY time ASC
                       LIMIT 120""", (current_batch["id"], params.get("last_timestamp") or 0))
        rows = cur.fetchall()
        return rows

def create_reading(conn, batch_id, step_id, reading):
    sql = ''' INSERT INTO batch_temperature_readings(temperature, fermentation_step_id, batch_id)
            VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (reading, step_id, batch_id))
    conn.commit()
    return cur.lastrowid

def seed_test_data(conn):
    create_batch(conn, ("Test Batch 1"))
    create_batch(conn, ("Test Batch 2"))
    create_step(conn, (17.0, 1624388158, 1624388278, 2))
    create_step(conn, (21.0, 1624388278, 1624388398, 2))
    create_step(conn, (24.0, 1624388398, 1624389058, 2))
