from flask import Flask, request, render_template, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('location.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            name TEXT PRIMARY KEY,
            latitude TEXT,
            longitude TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.json
    name = data.get('name')
    lat = data.get('latitude')
    lon = data.get('longitude')
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('location.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO locations (name, latitude, longitude, timestamp)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET
            latitude=excluded.latitude,
            longitude=excluded.longitude,
            timestamp=excluded.timestamp
    ''', (name, lat, lon, time))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Location saved'}), 200

@app.route('/locations')
def get_locations():
    conn = sqlite3.connect('location.db')
    c = conn.cursor()
    c.execute('SELECT name, latitude, longitude, timestamp FROM locations')
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
