import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')


@app.route('/api/alive', methods=['GET'])
def alive():
    return jsonify({"message": "Alive"}), 200

@app.route('/api/associations', methods=['GET'])
def get_associations():
    return jsonify(associations_df['id'].tolist()), 200


@app.route('/api/association/<int:id>', methods=['GET'])
def get_association(id):
    association = associations_df[associations_df['id'] == id]
    if association.empty:
        return jsonify({"error": "Association not found"}), 404
    return jsonify(association.to_dict(orient='records')[0]), 200


@app.route('/api/evenements', methods=['GET'])
def get_evenements():
    return jsonify(evenements_df['id'].tolist()), 200


@app.route('/api/evenement/<int:id>', methods=['GET'])
def get_evenement(id):
    evenement = evenements_df[evenements_df['id'] == id]
    if evenement.empty:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(evenement.to_dict(orient='records')[0]), 200


@app.route('/api/association/<int:id>/evenements', methods=['GET'])
def get_evenements_association(id):
    evenements = evenements_df[evenements_df['association_id'] == id]
    return jsonify(evenements.to_dict(orient='records')), 200

@app.route('/api/associations/type/<type>', methods=['GET'])
def get_associations_by_type(type):
    associations = associations_df[associations_df['type'] == type]
    return jsonify(associations.to_dict(orient='records')), 200
