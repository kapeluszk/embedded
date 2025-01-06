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