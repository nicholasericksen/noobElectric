from __future__ import absolute_import

# discrete calulcation
from __future__ import division
import numpy as np
import cv2
from pymongo import MongoClient
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from datetime import datetime


import cPickle
from bson.binary import Binary

from bson import json_util

from bson.objectid import ObjectId
from bson.raw_bson import RawBSONDocument

from flask_restful import reqparse
# from flask_compress import Compress
# compress = Compress()

parser = reqparse.RequestParser()

#import standard libraries
import os
import serial
import time
import simplejson as json
import bsonjs

# glcm imports
from skimage.filters import threshold_otsu
from skimage.feature import greycomatrix, greycoprops
from sklearn.feature_extraction import image

# Connect to mongodb
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.experiments
discreteLMP = db.meta
glcmData = db.glcm
histogramData = db.histograms
stokes_bgr = db.stokes_bgr
# from LMP import sensor_reading

# Import flask
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from flask_socketio import SocketIO
from flask_socketio import send, emit
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # app.run(threaded=True)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)
def datasummary(raw_data):
    data = raw_data.ravel()
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

def createhistogram(raw_data, bins):
    data = raw_data.ravel()
    # bins = np.arange(np.floor(data.min()),np.ceil(data.max()))
    hist = np.histogram(data, bins=bins)
    bins = bins.tolist()
    # / len(data) to normalize to 1
    values = hist[0] / len(data)

    # Convert the tuples into arrays for smaller formatting
    zipped = [list(t) for t in zip(bins, values.tolist())]

    return zipped

def calculate_stokes(P1, P2):
    P1 = P1.astype(np.int16)
    P2 = P2.astype(np.int16)

    S = (P1 - P2) / (P1 + P2)

    # These represent values that have not been illuminated by the source
    # ie they are the product of masking and shadowing.
    S[~np.isfinite(S)] = 0

    return S

def divide( a, b ):
    """ ignore / 0, div0( [-1, 0, 1], 0 ) -> [0, 0, 0] """
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.true_divide( a, b )
        c[ ~ np.isfinite( c )] = 0  # -inf inf NaN
    return c

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

@app.route('/api/experiments/tags', methods=['POST'])
def add_tags():
    print request.data

    exp_id = json.loads(request.data)['id'];
    print "EXO", exp_id
    tags = json.loads(request.data)['tags']
    print "tags", tags
    # data = discreteLMP.update_one({'_id': ObjectId(exp_id) }, {'tags': tags})
    # data_sanatized = json.loads(json_util.dumps(data))
    print data
    resp = jsonify({"exp": tags})
    print resp
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@app.route('/api/experiments/histograms', methods=['POST'])
def get_histograms_by_id():
    print "request.data", request.data

    exp_id = json.loads(request.data)['id'];
    data = histogramData.find_one({'meta_id': ObjectId(exp_id) })
    # print "data", data

    if not data:
        resp = jsonify({"exp": 'data_sanatized'})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    # data_sanatized = json.loads(json_util.dumps(data))
    # print cPickle.loads(data['histograms']['measurements']['V'])


    binary_convert = {}
    binary_convert['histograms'] = {}
    binary_convert['histograms']['measurements'] = {}

    binary_convert['meta_id'] = str(data['meta_id'])

    binary_convert['histograms']['measurements']['H'] = cPickle.loads(data['histograms']['measurements']['H'])
    binary_convert['histograms']['measurements']['V'] = cPickle.loads(data['histograms']['measurements']['V'])
    binary_convert['histograms']['measurements']['P'] = cPickle.loads(data['histograms']['measurements']['P'])
    binary_convert['histograms']['measurements']['M'] = cPickle.loads(data['histograms']['measurements']['M'])

    binary_convert['histograms']['stokes'] = {}
    binary_convert['histograms']['stokes']['S1'] = {}
    binary_convert['histograms']['stokes']['S2'] = {}
    binary_convert['histograms']['stokes']['S1']['data'] = cPickle.loads(data['histograms']['stokes']['S1']['data'])
    binary_convert['histograms']['stokes']['S1']['stats'] = cPickle.loads(data['histograms']['stokes']['S1']['stats'])

    binary_convert['histograms']['stokes']['S2']['data'] = cPickle.loads(data['histograms']['stokes']['S2']['data'])
    binary_convert['histograms']['stokes']['S2']['stats'] = cPickle.loads(data['histograms']['stokes']['S2']['stats'])

    data_sanatized = json.loads(json.dumps(binary_convert, cls=MyEncoder))

    resp = jsonify({"exp": data_sanatized})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    print "semt"
    return resp

@app.route('/api/experiments/histograms/bgr', methods=['POST'])
def get_bgr_histograms_by_id():
    print "request.data", request.data

    exp_id = json.loads(request.data)['id'];
    data = stokes_bgr.find_one({'meta_id': ObjectId(exp_id) })
    # print "data", data

    if not data:
        resp = jsonify({"exp": 'data_sanatized'})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    # data_sanatized = json.loads(json_util.dumps(data))
    # print cPickle.loads(data['histograms']['measurements']['V'])


    binary_convert = {}

    binary_convert['meta_id'] = str(data['meta_id'])

    binary_convert['histograms'] = {}
    binary_convert['histograms']['S1'] = {}
    binary_convert['histograms']['S1']['b'] = {}
    binary_convert['histograms']['S1']['g'] = {}
    binary_convert['histograms']['S1']['r'] = {}

    binary_convert['histograms']['S2'] = {}
    binary_convert['histograms']['S2']['b'] = {}
    binary_convert['histograms']['S2']['g'] = {}
    binary_convert['histograms']['S2']['r'] = {}

    binary_convert['histograms']['S1']['b']['data'] = cPickle.loads(data['histograms']['S1']['b']['data'])
    binary_convert['histograms']['S1']['b']['stats'] = cPickle.loads(data['histograms']['S1']['b']['stats'])
    binary_convert['histograms']['S1']['g']['data'] = cPickle.loads(data['histograms']['S1']['g']['data'])
    binary_convert['histograms']['S1']['g']['stats'] = cPickle.loads(data['histograms']['S1']['g']['stats'])
    binary_convert['histograms']['S1']['r']['data'] = cPickle.loads(data['histograms']['S1']['r']['data'])
    binary_convert['histograms']['S1']['r']['stats'] = cPickle.loads(data['histograms']['S1']['r']['stats'])

    binary_convert['histograms']['S2']['b']['data'] = cPickle.loads(data['histograms']['S2']['b']['data'])
    binary_convert['histograms']['S2']['b']['stats'] = cPickle.loads(data['histograms']['S2']['b']['stats'])
    binary_convert['histograms']['S2']['g']['data'] = cPickle.loads(data['histograms']['S2']['g']['data'])
    binary_convert['histograms']['S2']['g']['stats'] = cPickle.loads(data['histograms']['S2']['g']['stats'])
    binary_convert['histograms']['S2']['r']['data'] = cPickle.loads(data['histograms']['S2']['r']['data'])
    binary_convert['histograms']['S2']['r']['stats'] = cPickle.loads(data['histograms']['S2']['r']['stats'])
    print "about to sanitize"
    data_sanatized = json.loads(json.dumps(binary_convert, cls=MyEncoder))

    resp = jsonify({"exp": data_sanatized})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    print "sent"
    return resp

@app.route('/api/experiments/glcm', methods=['POST'])
def get_glcm_by_id():
    exp_id = json.loads(request.data)['id'];
    print "looking for glcm data"
    data = glcmData.find_one({'meta_id': ObjectId(exp_id), "size": 25 })
    print "found glcm data"
    if not data:
        print 'no data'
        resp = jsonify({"exp": 'binary_convert'})
        resp.headers['Access-Control-Allow-Origin'] = '*'

        return resp
    # print data
    # binary_convert = data
    # binary_convert['glcm'] = {}
    # binary_convert['glcm']['file'] = data['glcm']['file']
    # binary_convert['glcm']['dissimilarity'] = data['glcm']['dissimilarity']
    # binary_convert['glcm']['correlation'] = data['glcm']['correlation']
    # binary_convert['glcm']['asm'] = data['glcm']['asm']
    # binary_convert['glcm']['energy'] = data['glcm']['energy']
    # binary_convert['glcm']['contrast'] = data['glcm']['contrast']
    #
    # binary_convert['glcm']['S1'] = {}
    # binary_convert['glcm']['S2'] = {}
    print "converting glcm"
    data['glcm'] = cPickle.loads(data['glcm'])
    data['meta_id'] = data['meta_id']
    # print "done converting", data
    # binary_convert['glcm']['data'] = cPickle.loads(data['glcm']['data'])
    # binary_convert['size'] = 25
    # binary_convert['meta_id'] = ObjectId(exp_id)


    data_sanatized = json.loads(json_util.dumps(data))
    print "sanatized"
    resp = jsonify({"exp": data_sanatized})
    print "about to send resposne"
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

    dir_path = os.path.join(directory, filename)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(os.path.join(directory, filename), "wb") as fh:
        fh.write(stripped_image.decode('base64'))

    discrete = [f for f in os.listdir(directory) if f.endswith(".png")]


    resp = jsonify({"directory": directory, "images": discrete})
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@app.route('/api/data', methods=['GET'])
def get_data_directories():
    directories = [d for d in os.listdir('.') if os.path.isdir(d)]


    resp = jsonify({"data": directories})
    resp.headers['Access-Control-Allow-Origin'] = '*'


    return resp


@app.route('/api/generate/stokes', methods=['POST'])
def generate_discrete_stokes_data():
    raw_data = json.loads(request.data)
    exp_id = raw_data['id']
    images = raw_data['images']

    #set the directory the images come from
    imagedirectory = images

    H = cv2.imread(os.path.join(imagedirectory, 'H.png'), 1)
    V = cv2.imread(os.path.join(imagedirectory, 'V.png'), 1)
    P = cv2.imread(os.path.join(imagedirectory, 'P.png'), 1)
    M = cv2.imread(os.path.join(imagedirectory, 'M.png'), 1)

    H_gray = cv2.imread(os.path.join(imagedirectory, 'H.png'), 0)
    V_gray = cv2.imread(os.path.join(imagedirectory, 'V.png'), 0)
    P_gray = cv2.imread(os.path.join(imagedirectory, 'P.png'), 0)
    M_gray = cv2.imread(os.path.join(imagedirectory, 'M.png'), 0)

    S1 = calculate_stokes(H_gray, V_gray)
    S2 = calculate_stokes(P_gray, M_gray)

    print "S1", S1
    # Calculate the color channel stokes params
    Hb, Hg, Hr = cv2.split(H)
    Vb, Vg, Vr = cv2.split(V)
    Pb, Pg, Pr = cv2.split(P)
    Mb, Mg, Mr = cv2.split(M)

    S1b = calculate_stokes(Hb, Vb)
    S1g = calculate_stokes(Hg, Vg)
    S1r = calculate_stokes(Hr, Vr)

    S2b = calculate_stokes(Pb, Mb)
    S2g = calculate_stokes(Pg, Mg)
    S2r = calculate_stokes(Pr, Mr)

    # Save the images of the color channels
    # cv2.imwrite('img.png', img * 255)
    # cv2.imwrite('img.png', img * 255)
    # cv2.imwrite('img.png', img * 255)
    # cv2.imwrite('img.png', img * 255)
    # cv2.imwrite('img.png', img * 255)
    # cv2.imwrite('img.png', img * 255)

    # Create Histograms for the color stokes channels
    S1bsummary = datasummary(S1b)
    S1bzipped = createhistogram(S1b, np.linspace(-1,1,200))
    S1gsummary = datasummary(S1g)
    S1gzipped = createhistogram(S1g, np.linspace(-1,1,200))
    S1rsummary = datasummary(S1r)
    S1rzipped = createhistogram(S1r, np.linspace(-1,1,200))

    S2bsummary = datasummary(S2b)
    S2bzipped = createhistogram(S2b, np.linspace(-1,1,200))
    S2gsummary = datasummary(S2g)
    S2gzipped = createhistogram(S2g, np.linspace(-1,1,200))
    S2rsummary = datasummary(S2r)
    S2rzipped = createhistogram(S2r, np.linspace(-1,1,200))


    # Create summary for white light stokes
    S1summary = datasummary(S1)
    S1zipped = createhistogram(S1, np.linspace(-1,1,200))

    S2summary = datasummary(S2)
    S2zipped = createhistogram(S2, np.linspace(-1,1,200))

    # Create measurement Histograms
    Hzipped = createhistogram(H, np.arange(0, 256, 1))
    Vzipped = createhistogram(V, np.arange(0, 256, 1))
    Pzipped = createhistogram(P, np.arange(0, 256, 1))
    Mzipped = createhistogram(M, np.arange(0, 256, 1))
    # print Hzipped
    result = histogramData.insert_one(
        {
            'meta_id': ObjectId(exp_id),
            'histograms': {
                'measurements': {
                    'H': Binary(cPickle.dumps(Hzipped, protocol=2)),
                    'V': Binary(cPickle.dumps(Vzipped, protocol=2)),
                    'P': Binary(cPickle.dumps(Pzipped, protocol=2)),
                    'M': Binary(cPickle.dumps(Mzipped, protocol=2))
                },
                'stokes': {
                    'S1': {
                        'data': Binary(cPickle.dumps(S1zipped, protocol=2)),
                        'stats': Binary(cPickle.dumps(S1summary, protocol=2))
                    },
                    'S2': {
                        'data': Binary(cPickle.dumps(S2zipped, protocol=2)),
                        'stats': Binary(cPickle.dumps(S2summary, protocol=2))
                    }
                }
            }
        }
    )

    bgr_result = stokes_bgr.insert_one(
        {
            'meta_id': ObjectId(exp_id),
            'histograms': {
                'S1': {
                    'b': {
                        'data': Binary(cPickle.dumps(S1bzipped, protocol=2)),
                        'stats': Binary(cPickle.dumps(S1bsummary, protocol=2))
                    },
                    'g': {
                        'data': Binary(cPickle.dumps(S1gzipped, protocol=2)),
                        'stats': Binary(cPickle.dumps(S1gsummary, protocol=2))
                    },
                    'r': {
                        'data': Binary(cPickle.dumps(S1rzipped, protocol=2)),
                        'stats': Binary(cPickle.dumps(S1rsummary, protocol=2))
                    }

                },
                'S2': {
                    'b': {
                        'data': Binary(cPickle.dumps(S2bzipped, protocol=2)),
                        'stats': Binary(cPickle.dumps(S2bsummary, protocol=2))
                    },
                    'g': {
                        'data': Binary(cPickle.dumps(S2gzipped, protocol=2)),
                        'stats': Binary(cPickle.dumps(S2gsummary, protocol=2))
                    },
                    'r': {
                        'data': Binary(cPickle.dumps(S2rzipped, protocol=2)),
                        'stats': Binary(cPickle.dumps(S2rsummary, protocol=2))
                    }
                }
            }
        }
    )

    print "about to send response", result.inserted_id
    add_meta = discreteLMP.update_one(
        {
            '_id': ObjectId(exp_id)
        },
        {
            '$set': {
                'stokes': ObjectId(str(result.inserted_id)),
                'stokes_bgr': ObjectId(str(bgr_result.inserted_id))
            }
        }

    )
    print "updated"
    resp = jsonify({"data": 'Successfully inserted'})
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@app.route('/api/generate/glcm', methods=['POST'])
def generate_discrete_glcm_samples():
    raw_data = json.loads(request.data)
    exp_id = raw_data['id']
    images = raw_data['images']

    EXPERIMENT_DIR = images
    #Read the images for discrete analysis and flatten them
    Hraw = cv2.imread(EXPERIMENT_DIR + '/H.png', 0)
    Vraw = cv2.imread(EXPERIMENT_DIR + '/V.png', 0)
    Praw = cv2.imread(EXPERIMENT_DIR + '/P.png', 0)
    Mraw = cv2.imread(EXPERIMENT_DIR + '/M.png', 0)

    SAMPLE_SIZE = 500
    print "HELLO"
    PATCH_WINDOWS = [25]
    for size in PATCH_WINDOWS:
        print size

    Hpatches = {}
    Vpatches = {}
    Ppatches = {}
    Mpatches = {}
    # Pdry = cv2.imread('sandpaper-brown-60-grit/90.png', 0)
    # Pwet = cv2.imread('sandpaper-100-grit-brown-red-filter/90.png', 0)


    directory = EXPERIMENT_DIR + '/samples/'
    for size in PATCH_WINDOWS:
        dataset = []
        print "size", size
        Hpatches[str(size)] = image.extract_patches_2d(Hraw, (size, size), SAMPLE_SIZE, 1)
        Ppatches[str(size)] = image.extract_patches_2d(Praw, (size, size), SAMPLE_SIZE, 1)
        Vpatches[str(size)] = image.extract_patches_2d(Vraw, (size, size), SAMPLE_SIZE, 1)
        Mpatches[str(size)] = image.extract_patches_2d(Mraw, (size, size), SAMPLE_SIZE, 1)

        for index, Ppatch in enumerate(Ppatches[str(size)]):
            filenameP = directory + 'P-'+ str(size)+'-sample-' + str(index) + '.png'
            cv2.imwrite(filenameP, Ppatches[str(size)][index])
        for index, Mpatch in enumerate(Mpatches[str(size)]):
            filenameM = directory + 'M'+ str(size)+'-sample-' + str(index) + '.png'
            cv2.imwrite(filenameM, Mpatches[str(size)][index])

        for index, Vpatch in enumerate(Vpatches[str(size)]):
            filenameV = directory + 'V'+ str(size)+'-sample-' + str(index) + '.png'
            cv2.imwrite(filenameV, Vpatches[str(size)][index])


        for index, Hpatch in enumerate(Hpatches[str(size)]):
            try:
                glcm = greycomatrix(Hpatch, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4], 256, symmetric=True, normed=True)
                dissimilarity = greycoprops(glcm, 'dissimilarity')[0, 0]
                contrast = greycoprops(glcm, 'contrast')[0, 0]
                correlation = greycoprops(glcm, 'correlation')[0, 0]
                asm = greycoprops(glcm, 'ASM')[0, 0]
                energy = greycoprops(glcm, 'energy')[0, 0]

                glcm_data = {
                    'dissimilarity': dissimilarity,
                    'contrast': contrast,
                    'correlation': correlation,
                    'asm': asm,
                    'energy': energy
                }

                if not os.path.exists(directory):
                    os.makedirs(directory)

                filename = directory + 'H'+ str(size)+'-sample-' + str(index) + '.png'
                cv2.imwrite(filename, Hpatches[str(size)][index])

                H = Hpatches[str(size)][index].ravel()
                V = Vpatches[str(size)][index].ravel()
                P = Ppatches[str(size)][index].ravel()
                M = Mpatches[str(size)][index].ravel()

                S1 = divide((H - V), (H + V))
                S2 = divide((P - M), (P + M))

                S1summary = datasummary(S1)
                S2summary = datasummary(S2)

                # Create the S1 and S2 Histogram
                S1zipped = createhistogram(S1, np.arange(-1, 1.01, 0.01))
                S2zipped = createhistogram(S2, np.arange(-1, 1.01, 0.01))

                S1obj = {
                    "data": S1zipped,
                    "stats": S1summary
                }

                S2obj = {
                    "data": S2zipped,
                    "stats": S1summary
                }
                S = [list(t) for t in zip(S1, S2)]

                stokes = {
                    'filename': filename,
                    'S1': S1obj,
                    'S2': S2obj
                }


                # data = {
                #     'stokes': stokes,
                #     'data': glcm_data
                # }



                # binary_convert['glcm']['file'] = str(filename)
                # binary_convert['glcm']['dissimilarity'] = dissimilarity
                # binary_convert['glcm']['correlation'] = correlation
                # binary_convert['glcm']['asm'] = asm
                # binary_convert['glcm']['energy'] = energy
                # binary_convert['glcm']['contrast'] = contrast
                # binary_convert['glcm']['S1'] = Binary(cPickle.dumps(S1obj, protocol=2))
                # binary_convert['glcm']['S2'] = Binary(cPickle.dumps(S2obj, protocol=2))
                # binary_convert['size'] = size
                # binary_convert['meta_id'] = ObjectId(exp_id)

                # dataset.append(data)


                glcm_data = {
                        'meta_id': ObjectId(exp_id),
                        'glcm': glcm_data,
                        'window_size': size,
                        'stokes': stokes
                }

                result = glcmData.insert_one(glcm_data)

            except ValueError:
                print "ERROR"
                pass

        # add_meta = discreteLMP.update_one(
        #     {
        #         '_id': ObjectId(exp_id)
        #     },
        #     {
        #         '$set': {
        #             'glcm': ObjectId(str(result.inserted_id))
        #         }
        #     }
        #
        # )
    print "about to send response"
    resp = jsonify({"data": 'Successfully inserted'})
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@app.route('/api/experiments/new', methods=['POST'])
def upload_new_discrete_LMP():
    raw_data = json.loads(request.data)

    title = raw_data['title']
    summary = raw_data['summary']
    description = raw_data['description']
    images = raw_data['images']

    result = discreteLMP.insert_one(
        {
            "title": title,
            "summary": summary,
            "description": description,
            "date": str(datetime.utcnow()),
            "images": images
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


@socketio.on('request_glcm_samples', namespace='/test')
def paginate_glcm_samples(request_data):
    # exp_id = json.loads(request.data)['id'];
    print "SOCET", request_data
    exp_id = json.loads(request_data)['id']
    print "looking for glcm data", exp_id
    loading = True
    skip = json.loads(request_data)['skip']
    limit = json.loads(request_data)['limit']



    # while(loading):
    data = glcmData.find({'meta_id': ObjectId(exp_id), "window_size": 25 })
    if not data:
        print 'no data'
        resp = jsonify({"exp": 'binary_convert'})
        resp.headers['Access-Control-Allow-Origin'] = '*'

        return resp
    # print data
    # binary_convert = data
    # binary_convert['glcm'] = {}
    # binary_convert['glcm']['file'] = data['glcm']['file']
    # binary_convert['glcm']['dissimilarity'] = data['glcm']['dissimilarity']
    # binary_convert['glcm']['correlation'] = data['glcm']['correlation']
    # binary_convert['glcm']['asm'] = data['glcm']['asm']
    # binary_convert['glcm']['energy'] = data['glcm']['energy']
    # binary_convert['glcm']['contrast'] = data['glcm']['contrast']
    #
    # binary_convert['glcm']['S1'] = {}
    # binary_convert['glcm']['S2'] = {}
    # print "converting glcm", list(data[1:4])



    # data[0]['glcm'] = cPickle.loads(data[0]['glcm'])
    # data[0]['meta_id'] = data[0]['meta_id']

    # print cPickle.loads(data[0]['glcm'])
    # print "done converting", data
    # binary_convert['glcm']['data'] = cPickle.loads(data['glcm']['data'])
    # binary_convert['size'] = 25
    # binary_convert['meta_id'] = ObjectId(exp_id)
    paginate = data

    data_sanatized = json.loads(json_util.dumps(list(paginate[skip:limit])))
    # print "sanatized", data_sanatized
    resp = {"exp": data_sanatized}
    print "SEND"
    if limit < 500:
        print "DONE DONE"
        # resp.headers['Access-Control-Allow-Origin'] = '*'
        emit('glcm_sent', resp, namespace='/test')
    else:
        print "blah"
    # resp = jsonify({"exp": 'binary_convert'})
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    #
    # return resp
        # skip = limit
        # print "skip", skip
        # print "limit", limit
        # limit += 50

        # if limit > 500:
        #     loading = False
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
    socketio.run(app, debug=True)
  # socketio.run(app)
