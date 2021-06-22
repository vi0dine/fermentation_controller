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
        seed_test_data(conn)
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
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            ); """)
        c.execute("""CREATE TABLE IF NOT EXISTS fermentation_steps (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                current integer DEFAULT 0,
                                temperature real NOT NULL,
                                begin_date TIMESTAMP NOT NULL,
                                end_date TIMESTAMP NOT NULL,
                                batch_id integer NOT NULL,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (batch_id) REFERENCES batches (id)
                            );""")
        c.execute("""CREATE TABLE IF NOT EXISTS batch_temperature_readings (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                temperature real NOT NULL,
                                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
    cur.execute(sql, batch)
    conn.commit()
    return cur.lastrowid

def update_batch(conn, batch):
    cur = conn.cursor()
    if batch["current"] == 1:
        cur.execute("""UPDATE batches SET current = 0""")

    cur.execute("""UPDATE batches SET name = ?, current = ? WHERE id = ?""", (batch["name"], batch["current"]))
    conn.commit()
    
    return cur.lastrowid

def get_steps(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM batches WHERE current = 1")

    current_batch = cur.fetchone()

    if current_batch:
        cur.execute("SELECT * FROM fermentation_steps WHERE batch_id = ? ORDER BY start_date ASC", (current_batch["id"],))
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

def set_step_as_current(conn, step_id):
    cur = conn.cursor()
    cur.execute("UPDATE fermentation_steps SET current = 0")
    cur.execute("UPDATE fermentation_steps SET current = 1 WHERE id = ?", (batch_id,))

def get_readings(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM batches WHERE current = 1")
    current_batch = cur.fetchone()

    if current_batch:
        cur.execute("SELECT * FROM batch_temperature_readings WHERE batch_id = ?", (current_batch["id"],))
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
    create_batch(conn, ("Test Batch 1", 0))
    create_batch(conn, ("Test Batch 2", 1))
    create_step(conn, (17.0, 1624289246, 1624462046, 2, 0))
    create_step(conn, (21.0, 1624462046, 1624807646, 2, 0))
    create_step(conn, (24.0, 1624807646, 1624907646, 2, 0))