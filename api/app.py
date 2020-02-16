from flask import Flask, request, abort, Response
# from flask_cors import CORS
import numpy as np

app = Flask(__name__)
# CORS(app)

# Wald's maximin model
@app.route('/classic/wald', methods=['POST'])
def wald():
    if not request.json or not 'matrix' in request.json:
        abort(400)
    raw_matrix = request.json['matrix']
    matrix = np.array(raw_matrix)
    print(matrix)
    try: 
        raw_of_mins = matrix.min(axis=1)
        number_station = raw_of_mins.argmax() + 1
        crit = raw_of_mins.max()
    except:
        abort(422)
    return 'Станция {}. Критерий = {}'.format(number_station, crit)

# Критерий азартного игрока
@app.route('/classic/maximax', methods=['POST'])
def maximax():
    if not request.json or not 'matrix' in request.json:
        abort(400)
    raw_matrix = request.json['matrix']
    matrix = np.array(raw_matrix)
    try:
        raw_of_maxs = matrix.max(axis=1)
        number_station = raw_of_maxs.argmax() + 1
        crit = raw_of_maxs.max()
    except:
        abort(422)
    return 'Станция {}. Критерий = {}'.format(number_station, crit)