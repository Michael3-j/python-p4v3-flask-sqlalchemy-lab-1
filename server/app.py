#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = db.session.get(Earthquake, id)  # Using session.get() to avoid deprecation warnings
    if earthquake:
        return jsonify(earthquake.to_dict()), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

# New view for filtering earthquakes by magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quake_list = [quake.to_dict() for quake in quakes]
    
    response = {
        "count": len(quake_list),
        "quakes": quake_list
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)



