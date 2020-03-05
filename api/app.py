from flask import Flask, request, abort, Response
# from flask_cors import CORS
import numpy as np
import math
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

# Routh–Hurwitz stability criterion
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

# Laplace’s insufficient reason criterion
@app.route('/classic/laplace', methods=['POST'])
def laplace():
    if not request.json or not 'matrix' in request.json:
        abort(400)
    raw_matrix = request.json['matrix']
    matrix = np.array(raw_matrix)
    try:
        vector_of_averages = matrix.mean(axis=1)
        number_station = vector_of_averages.argmax() + 1
        crit = vector_of_averages.max()
    except:
        abort(422)
    return result_str(number_station, crit)

# modified Hurwitz stability criterion 
# f_crit hardcoded !!!
@app.route('/classic/hurwitz_mod', methods=['POST'])
# TODO: DRY
def hurwitz_mod():
    if not request.json or not 'matrix' in request.json:
        abort(400)
    raw_matrix = request.json['matrix']
    matrix = np.array(raw_matrix)
    try:
        vector_of_mins = matrix.min(axis=1)
        wald_crit = vector_of_mins.max()
        vector_of_averages = matrix.mean(axis=1)
        f_crit = wald_crit * 0.6 
        bool_vector_of_alternatives = vector_of_averages <= f_crit ### so we don't lose the numbering
        vector_of_averages[bool_vector_of_alternatives] = -math.inf ### 
        number_station = vector_of_averages.argmax() + 1
        crit = vector_of_averages.max()
    except:
        abort(422)
    return result_str(number_station, crit)

# Критерий Гермейера
@app.route('/probability/germeier', methods=['POST'])
def germeier():
    if not request.json or not 'matrix' in request.json or not 'probability':
        abort(400)
    raw_matrix = request.json['matrix']
    matrix = np.array(raw_matrix)
    raw_propability = request.json['probability']
    propability = np.array(raw_propability)
    try:
        matrix = matrix - matrix.max() - 1
        criter_min = matrix.min(axis=0) * propability
        number_station = criter_min.argmax() + 1
        crit = criter_min.max()
    except:
        abort(422)
    return result_str(number_station, crit)