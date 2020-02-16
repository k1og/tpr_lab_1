from flask import Flask, request, abort, Response
# from flask_cors import CORS
import numpy as np

app = Flask(__name__)
# CORS(app)

def result_str(number_station, crit):
    return 'Станция {}. Критерий = {}'.format(number_station, crit)

# Wald's maximin model
@app.route('/classic/wald', methods=['POST'])
def wald():
    if not request.json or not 'matrix' in request.json:
        abort(400)
    raw_matrix = request.json['matrix']
    matrix = np.array(raw_matrix)
    print(matrix)
    try: 
        vector_of_mins = matrix.min(axis=1)
        number_station = vector_of_mins.argmax() + 1
        crit = vector_of_mins.max()
    except:
        abort(422)
    return result_str(number_station, crit)

# Критерий азартного игрока
@app.route('/classic/maximax', methods=['POST'])
def maximax():
    if not request.json or not 'matrix' in request.json:
        abort(400)
    raw_matrix = request.json['matrix']
    matrix = np.array(raw_matrix)
    try:
        vector_of_maxes = matrix.max(axis=1)
        number_station = vector_of_maxes.argmax() + 1
        crit = vector_of_maxes.max()
    except:
        abort(422)
    return result_str(number_station, crit)

#Routh–Hurwitz stability criterion
@app.route('/classic/hurwitz', methods=['POST'])
def hurwitz():
    if not request.json or not 'matrix' in request.json or not 'alpha' in request.json:
        abort(400)
    alpha = request.json['alpha']
    if alpha < 0 or alpha > 1:
        abort(422)
    raw_matrix = request.json['matrix']
    matrix = np.array(raw_matrix)
    try:
        vector_of_maxes = matrix.max(axis=1)
        vector_of_mins = matrix.min(axis=1)
        pessimism_coef = 1 - alpha
        optimism_coef = alpha
        matrix_of_winnings = optimism_coef * vector_of_maxes + pessimism_coef * vector_of_mins
        number_station = matrix_of_winnings.argmax() + 1
        crit = matrix_of_winnings.max()
    except:
        abort(422)
    return result_str(number_station, crit)