from flask import Flask, jsonify
import json
import os, sys

p = os.path.abspath('.')
sys.path.insert(1, p)

from database import db

app = Flask(__name__)


@app.route('/api/batches')
def batches():
    conn = db.create_connection(r"./brew_valley_link.db")
    batches = db.get_batches(conn)
    return json.dumps(batches)

@app.route('/api/steps')
def steps():
    conn = db.create_connection(r"./brew_valley_link.db")
    steps = db.get_steps(conn)
    return json.dumps(steps)

@app.route('/api/readings')
def readings():
    conn = db.create_connection(r"./brew_valley_link.db")
    readings = db.get_readings(conn)
    return json.dumps(readings)

if __name__ == '__main__':
    app.run(debug=True, port=4000, host='0.0.0.0')