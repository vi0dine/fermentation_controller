from flask import Flask, request, Response
from flask_cors import CORS
from functools import wraps
import json
import db

app = Flask(__name__)
CORS(app)

def login_required(f):
    @wraps(f)
    def wrapped_view(**kwargs):
        auth = request.authorization
        if not (auth and check_auth(auth.username, auth.password)):
            return ('Unauthorized', 401, {
                'WWW-Authenticate': 'Basic realm="Login Required"'
            })

        return f(**kwargs)

    return wrapped_view

def check_auth(username, password):
    return username == 'test' and password == 'test'


@app.route('/api/batches', methods=['GET', 'POST'])
@login_required
def batches():
    if request.method == 'GET':
        conn = db.create_connection(r"./brew_valley_link.db")
        batches = db.get_batches(conn)
        return render_json(batches)
    else:
        data = request.get_json(force=True)
        conn = db.create_connection(r"./brew_valley_link.db")
        batch = db.create_batch(conn, (data["name"],))
        return render_json(batch, 201)

@app.route('/api/batches/<id>', methods=['PUT'])
@login_required
def batch(id):
    data = request.get_json(force=True)
    conn = db.create_connection(r"./brew_valley_link.db")
    batch = db.update_batch(conn, {"id": id, "name": data["name"], "current": data["current"] })
    return render_json(batch)


@app.route('/api/steps', methods=['GET', 'POST'])
@login_required
def steps():
    if request.method == 'GET':
        conn = db.create_connection(r"./brew_valley_link.db")
        steps = db.get_steps(conn)
        return render_json(steps)
    else:
        data = request.get_json(force=True)
        conn = db.create_connection(r"./brew_valley_link.db")
        step = db.create_step(conn, (data["temperature"], data["begin_date"], data["end_date"], data["batch_id"]))
        return render_json(step, 201)

@app.route('/api/steps/<id>', methods=['PUT'])
@login_required
def step(id):
    data = request.get_json(force=True)
    conn = db.create_connection(r"./brew_valley_link.db")
    step = db.update_step(conn, {"id": id, "temperature": data["temperature"], "current": data["current"], "begin_date": data["begin_date"], "end_date": data["end_date"] })
    return render_json(step)

@app.route('/api/readings')
@login_required
def readings():
    conn = db.create_connection(r"./brew_valley_link.db")
    readings = db.get_readings(conn)
    return render_json(readings)

def render_json(response, status=200):
    r = Response(json.dumps(response), status, mimetype="application/json")
    return r

if __name__ == '__main__':
    app.run(debug=True, port=4001, host='0.0.0.0')