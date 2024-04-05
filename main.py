from flask import Flask, render_template, request, jsonify
from tinydb import TinyDB, Query
from pydobot import Dobot
import serial.tools.list_ports

app = Flask(__name__)
db = TinyDB('db.json')


def init_robot_connection():
    port = 'COM10'
    try:
        return Dobot(port=port, verbose=False), True
    except (serial.serialutil.SerialException, OSError):
            print('porta errada')
            return None, False


@app.route('/')
def index():
    global robot, connected
    robot, connected = init_robot_connection()
    logs = db.all()
    return render_template('index.html', logs=logs, connected=connected)

@app.route('/move-up', methods=['GET'])
def move_up():
    if connected and robot is not None:
        try:
            (x, y, z, r, j1, j2, j3, j4) = robot.pose()
            robot.move_to(x, y, z + 40, r, wait=True)
            db.insert({'command': 'move-up'})
            return jsonify({'success': 'Moved up'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Robô não conectado'}), 400

@app.route('/move-down', methods=['GET'])
def move_down():
    if robot:
        (x, y, z, r, j1, j2, j3, j4) = robot.pose()
        robot.move_to(x,y,z-40,r)
        db.insert({'command': 'move-down'})
        return jsonify({'success': 'Moved down'}), 200
    else:
        return jsonify({'error': 'Robô não conectado'}), 400

@app.route('/delete-logs', methods=['GET'])
def delete_logs():
    db.truncate()
    return jsonify({'success': 'Logs deleted'}), 200

@app.route('/get_logs', methods=['GET'])
def get_logs():
    logs = db.all()
    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True)
