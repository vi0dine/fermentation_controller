from flask import Flask, request, Response
import json
import db

app = Flask(__name__)


@app.route('/api/batches', methods=['GET', 'POST'])
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
def batch(id):
    data = request.get_json(force=True)
    conn = db.create_connection(r"./brew_valley_link.db")
    batch = db.update_batch(conn, {"id": id, })
    return render_json(batch)


@app.route('/api/steps')
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
def step(id):
    conn = db.create_connection(r"./brew_valley_link.db")
    step = db.set_step_as_current(conn, id)
    return render_json(batch)

@app.route('/api/readings')
def readings():
    conn = db.create_connection(r"./brew_valley_link.db")
    readings = db.get_readings(conn)
    return render_json(readings)

def render_json(response, status=200):
    r = Response(json.dumps(response), status, mimetype="application/json")
    return r

if __name__ == '__main__':
    app.run(debug=True, port=4001, host='0.0.0.0')