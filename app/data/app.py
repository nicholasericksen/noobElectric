from __future__ import absolute_import

from bson import json_util
from bson.objectid import ObjectId

from flask_restful import reqparse

parser = reqparse.RequestParser()

import os
import serial
import time
import json

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.experiments
discreteLMP = db.discrete
# from LMP import sensor_reading

from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app)

# port = "/dev/cu.usbmodem1411"
# baudrate = 9600
# angle = [0, 90, 45, -45, "LCP", "RCP"]
# ser = serial.Serial(port, baudrate)
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/')
def hello_world():
  return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api')
def api():
    data_array = []

    for data in discreteLMP.find():
        data_array.append(data)
    # jsonify({"id": v for k, v in data.items() if k == '_id'}))
    data_sanatized = json.loads(json_util.dumps(data_array))
    resp = jsonify({"exp": data_sanatized})
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp
#
@app.route('/api/experiments', methods=['POST'])
def get_exp_by_id():
    print request.data

    exp_id = json.loads(request.data)['id'];
    data = discreteLMP.find_one({'_id': ObjectId(exp_id) })
    data_sanatized = json.loads(json_util.dumps(data))

    resp = jsonify({"exp": data_sanatized})
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@app.route('/api/saveimage', methods=['POST'])
def save_base64_image():
    raw_data = json.loads(request.data)

    image = str(raw_data['data'])
    directory = raw_data['directory']
    filename = raw_data['filename'] + ".png"
    # print image
    stripped_image = image.split(",")[1]

    print directory

    dir_path = os.path.join(directory, filename)

    print dir_path

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(os.path.join(directory, filename), "wb") as fh:
        fh.write(stripped_image.decode('base64'))

    discrete = [f for f in os.listdir(directory) if f.endswith(".png")]

    print discrete

    resp = jsonify({"directory": directory, "images": discrete})
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@app.route('/api/data', methods=['GET'])
def get_data_directories():
    directories = [d for d in os.listdir('.') if os.path.isdir(d)]

    print directories

    resp = jsonify({"data": directories})
    resp.headers['Access-Control-Allow-Origin'] = '*'

    print resp

    return resp


@app.route('/api/experiments/new', methods=['POST'])
def upload_new_discrete_LMP():
    raw_data = json.loads(request.data)

    title = raw_data['title']
    summary = raw_data['summary']
    description = raw_data['description']
    images = raw_data['images']

    
# @app.route('/upload', methods=['POST'])
# def file_upload():
#
#     print request
#
#     if 'file' not in request.files:0
#         print 'No file part'
#         return redirect(request.url)
#     file = request.files['file']
#     # if user does not select file, browser also
#     # submit a empty part without filename
#     if file.filename == '':
#         print 'No selected file'
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         print 'File Upload Successful'
#         return redirect('/')

task = [{'test': 'test'}]

@app.route('/upload', methods=['GET'])
def retrieve_files():
    exp = []

    for f in os.listdir('uploads'):
        if not f.startswith('.'):
            exp.extend(f)

    # experiments = os.listdir('./uploads')
    return jsonify({"exp": exp})


# def retrieve_exp_description(exp):
#     with open('uploads/' + exp + '/info.txt', 'r') as myfile:
#         info = myfile.read()
#         print info



# @app.route('/lightsensor')
# def get_reading():
#     # sensor_reading()
#
#     time.sleep(2)
#
#     ser.flush()
#     ser.write('3')
#
#     time.sleep(1)
#
#     measurement = ser.readline()
#
#     return measurement
#
#
# @app.route('/motor', methods=['POST'])
# def motor():
#     data = request.get_json()
#     direction = data.get('dir')
#
#     time.sleep(2)
#     ser.flush()
#
#     if direction == 'left':
#         ser.write('4')
#     if direction == 'right':
#         ser.write('5')
#     # ser.write('4')
#     time.sleep(1)
#
#     return 'successful'

# @socketio.on('sensor reading', namespace='/test')
# def sensor_reading():
#     num = 0
#     while True:
#         num = num + 1
#         socketio.emit('reading', {'num': num}, namespace='/test')

@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)
  # socketio.run(app)
