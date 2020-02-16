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
    try: 
        number_station = matrix.min(axis=1).argmax() + 1
        crit = matrix.min(axis=1).max()
    except:
        abort(422)
    return 'Станция {}. Критерий = {}'.format(number_station, crit)