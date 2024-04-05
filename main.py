from flask import Flask, render_template, request, jsonify
from tinydb import TinyDB, Query
from pydobot import Dobot
import serial.tools.list_ports

app = Flask(__name__)
db = TinyDB('db.json')
global robot, connected 
try:
    robot = Dobot(port='COM10', verbose=False)
    connected = True
    print('')
except (serial.serialutil.SerialException, OSError):
    connected = False
    print('porta errada')


@app.route('/')
def index(): 
    logs = db.all()
    return render_template('index.html', logs=logs, connected=connected)

@app.route('/move-up', methods=['POST'])
def move_up():
    if robot:
        (x, y, z, r, j1, j2, j3, j4) = robot.pose()
        db.insert({'command': 'move-up'})
        return robot.move_to(x,y,z+40,r)
    else:
        return jsonify({'error': 'Robô não conectado'}), 400

@app.route('/move-down', methods=['POST'])
def move_down():
    if robot:
        (x, y, z, r, j1, j2, j3, j4) = robot.pose()
        robot.move_to(x,y,z-40,r)
        db.insert({'command': 'move-down'})
        return robot.move_to(x,y,z-40,r)
    else:
        return jsonify({'error': 'Robô não conectado'}), 400

@app.route('/delete-logs', methods=['POST'])
def delete_logs():
    return db.truncate()

@app.route('/get_logs', methods=['GET'])
def get_logs():
    logs = db.all()
    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True)
