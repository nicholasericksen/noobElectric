from __future__ import absolute_import

# discrete calulcation
from __future__ import division
import numpy as np
import cv2
from pymongo import MongoClient
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from datetime import datetime



from bson import json_util
from bson.objectid import ObjectId

from flask_restful import reqparse

parser = reqparse.RequestParser()

#import standard libraries
import os
import serial
import time
import json

# Connect to mongodb
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.experiments
discreteLMP = db.meta
glcmData = db.glcm
histogramData = db.histograms
# from LMP import sensor_reading

# Import flask
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from flask_socketio import SocketIO
from flask_socketio import send, emit
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.run(threaded=True)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def datasummary(data):
    maxValue = np.amax(data)
    minValue = np.amin(data)
    length = len(data)
    mean = np.mean(data)
    std = np.std(data)

    return {
        "max": maxValue,
        "min": minValue,
        "mean": mean,
        "std": std,
        "numpts": length
    }

def createhistogram(data, bins):
    hist = np.histogram(data, bins=bins)
    bins = hist[1].tolist()
    values = hist[0].tolist()

    # Convert the tuples into arrays for smaller formatting
    zipped = [list(t) for t in zip(bins, values)]

    return zipped

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

@app.route('/api/experiments/histograms', methods=['POST'])
def get_histograms_by_id():
    print request.data

    exp_id = json.loads(request.data)['id'];
    data = histogramData.find_one({'meta_id': ObjectId(exp_id) })
    data_sanatized = json.loads(json_util.dumps(data))

    resp = jsonify({"exp": data_sanatized})
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@app.route('/api/experiments/glcm', methods=['POST'])
def get_glcm_by_id():
    print request.data

    exp_id = json.loads(request.data)['id'];
    data = glcmData.find_one({'meta_id': ObjectId(exp_id) })
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

    float_formatter = lambda x: "%.2f" % x
    np.set_printoptions(formatter={'float_kind':float_formatter})

    #set the directory the images come from
    imagedirectory = images

    Hraw = np.array(cv2.imread(os.path.join(imagedirectory, 'H.png'), 0).ravel(), dtype=np.float32)
    Vraw = np.array(cv2.imread(os.path.join(imagedirectory, 'V.png'), 0).ravel(), dtype=np.float32)
    Praw = np.array(cv2.imread(os.path.join(imagedirectory, 'P.png'), 0).ravel(), dtype=np.float32)
    Mraw = np.array(cv2.imread(os.path.join(imagedirectory, 'M.png'), 0).ravel(), dtype=np.float32)

    zeroindex = []
    index = 0
    while (index < len(Hraw)):
        # Remove if all are 0 and/or Nan values
        if (Hraw[index] == 0 or np.isnan(Hraw[index])) and (Vraw[index] == 0 or np.isnan(Vraw[index])) or (Praw[index] == 0 or np.isnan(Praw[index])) and (Mraw[index] == 0 or np.isnan(Mraw[index])):
            zeroindex.append(index)
        index += 1

    print 'Number of points removed: ', len(zeroindex)

    # Remove values from all arrays equally so as to retain the size
    H = np.delete(Hraw, zeroindex, axis=0)
    V = np.delete(Vraw, zeroindex, axis=0)
    P = np.delete(Praw, zeroindex, axis=0)
    M = np.delete(Mraw, zeroindex, axis=0)

    # Calculate the Stokes parameters
    # Power intensities are taken and normalized
    S1 = (H - V) / (H + V)
    S2 = (P - M) / (P + M)


    # Print statistics about Stokes data
    S1summary = datasummary(S1)
    S2summary = datasummary(S2)

    # Create the S1 and S2 Histogram
    S1zipped = createhistogram(S1, np.arange(-1, 1.01, 0.01))
    S2zipped = createhistogram(S2, np.arange(-1, 1.01, 0.01))

    # Create measurement Histograms
    Hzipped = createhistogram(H, np.arange(0, 256, 1))
    Vzipped = createhistogram(V, np.arange(0, 256, 1))
    Pzipped = createhistogram(P, np.arange(0, 256, 1))
    Mzipped = createhistogram(M, np.arange(0, 256, 1))


    result = discreteLMP.insert_one(
        {
            "title": title,
            "summary": summary,
            "description": description,
            "date": str(datetime.utcnow()),
            "images": images,
            "histograms": {
                "measurements": {
                    "H": jsonify(Hzipped),
                    "V": jsonify(Vzipped),
                    "P": jsonify(Pzipped),
                    "M": jsonify(Mzipped)
                },
                "stokes": {
                    "S1": {
                        "data": jsonify(S1zipped),
                        "stats": jsonify(S1summary)
                    },
                    "S2": {
                        "data": jsonify(S2zipped),
                        "stats": jsonify(S2summary)
                    }
                }
            }
        }
    )

    resp = jsonify({"data": 'Successfully inserted'})
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

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
# def sensor_reading():
#     port = "/dev/cu.usbmodem1411"
#     baudrate = 9600
#     # angle = [0, 90, 45, -45, "LCP", "RCP"]
#     ser = serial.Serial(port, baudrate)
#
#     # time.sleep(1)
#
#     # ser.flush()
#     # ser.write('3')
#
#     # time.sleep(1)
#
#     measurement = ser.readline()
#
#     print "Voltage", measurement
#
#     resp = jsonify({"data": measurement})
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#
#     return resp

# @socketio.on('message')
# def handle_message(message):
#     port = "/dev/cu.usbmodem1411"
#     baudrate = 9600
#     # angle = [0, 90, 45, -45, "LCP", "RCP"]
#     ser = serial.Serial(port, baudrate)
#
#     # time.sleep(1)
#
#     # ser.flush()
#     # ser.write('3')
#
#     # time.sleep(1)
#     print message
#
#     measurement = ser.readline()
#     print measurement
#     emit('value', str(measurement))

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
  socketio.run(app)
  # socketio.run(app)
