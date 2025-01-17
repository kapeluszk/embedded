import sqlite3

def init_db(conn,cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Measurements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        temperature REAL NOT NULL,
        illuminance INTEGER NOT NULL,
        moisture INTEGER NOT NULL
    );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Plant_references (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_name TEXT NOT NULL,
        temperature REAL,
        illuminance REAL,
        moisture REAL
    );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS plant (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_name TEXT NOT NULL,
        target_moisture REAL
    );
    ''')
    cur.execute('''
        INSERT OR IGNORE INTO plant (plant_name, target_moisture) VALUES ('default', 10);
    ''')
    cur.execute('''
    INSERT OR IGNORE INTO Plant_references (plant_name, temperature, illuminance, moisture) VALUES ('Rhubarb', 21.7, 30, 4.75);
    ''')
    conn.commit()

def add_measurement(conn,cur, temperature, illuminance, moisture):
    try:
        cur.execute('''
            INSERT INTO Measurements (temperature, illuminance, moisture)
            VALUES (?, ?, ?)
        ''', (temperature, illuminance, moisture))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error adding measurement: {e}")

def fetch_measurements(cur, days):
    try:
        cur.execute(f"""
            SELECT * FROM Measurements
            WHERE timestamp >= DATETIME('now', '-{days} days')
        """)
        data = cur.fetchall()
        return data
    except sqlite3.Error as e:
        print(f"Error fetching measurements: {e}")
        return []

def fetch_plant_references(cur, plant_name):
    cur.execute(f"""SELECT temperature, illuminance, moisture FROM Plant_references WHERE plant_name = '{plant_name}'""")
    data = cur.fetchone()
    return data

def fetch_target_moisture(cur):
    cur.execute(f"""SELECT target_moisture FROM plant WHERE plant_name = 'default'""")
    data = cur.fetchone()
    return data

def fetch_current_moisture(cur):
    cur.execute(f"""SELECT moisture FROM Measurements ORDER BY timestamp DESC LIMIT 1""")
    data = cur.fetchone()
    return data

def update_target_moisture(conn,cur, target_moisture):
    try:
        cur.execute('''
            UPDATE plant
            SET target_moisture = ?
            WHERE plant_name = 'default'
        ''', (target_moisture,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating target moisture: {e}")