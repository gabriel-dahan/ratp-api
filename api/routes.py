from flask import jsonify

from . import app, api
from .models import RATP_Line

TRANSPORT_TYPES = ['metro', 'train', 'tramway', 'bus']

@app.route('/lines/<string:type>/', methods=['GET'])
def get_all_lines(type: str | None):
    """
    Get all lines of a specific type from the RATP network.
    ---
    parameters:
      - name: type
        in: path
        type: string
        required: false
        description: The type of transport (bus, train, metro, tramway).
    responses:
      200:
        description: OK
    """

    if type and type in TRANSPORT_TYPES:
        return jsonify(RATP_Line.query.filter_by(type = type).all())
    return jsonify(RATP_Line.query.all())

@app.route('/lines/<string:id>', methods = ['GET'])
def get_line(id: str):
    """
    Get line informations of a specific line from the RATP network.
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The code of transport line
    responses:
      200:
        description: OK
      400:
        description: Bad Request
    """

    line = RATP_Line.query.filter_by(id = id).first()

    if line:
        return jsonify(api.get_schedules(id))
    
    return jsonify({'error': 'This id is not in use or is incorrect.'})


@app.route('/lines/match/<string:name>')
def get_line_matches(name: str):
    """
    Get the 5 first matches of a line name in the RATP network.
    ---
    parameters:
      - name: name
        in: path
        type: string
        required: true
        description: The name of the line.
    responses:
      200:
        description: OK
      400:
        description: Bad Request
    """

    res = list(
        map(
            lambda x : x.serialize, 
            RATP_Line.query.filter(RATP_Line.name.like(f'%{name}%')).limit(5).all()
        )
    )
    return jsonify(res)

@app.route('/lines/<string:id>/destinations', methods=['GET'])
def get_line_destinations(id: str):
    """
    Get destinations of a specific line from the RATP network.
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The code of transport line
    responses:
      200:
        description: OK
      400:
        description: Bad Request
    """

    line = RATP_Line.query.filter_by(id = id).first()

    if line:
        return jsonify(api.get_stations(id))
    
    return jsonify({'error': 'This id is not in use or is incorrect.'})


@app.route('/traffic', methods=['GET'])
def get_traffic_all_lines():
    """
    Get traffic of all lines from the RATP network.
    ---
    responses:
      200:
        description: OK
    """

    return jsonify({'message': 'Traffic of all lines from RATP network'})


@app.route('/traffic/<string:type>', methods=['GET'])
def get_traffic_by_type(type):
    """
    Get traffic of a specific type of transport from the RATP network.
    ---
    parameters:
      - name: type
        in: path
        type: string
        required: true
        description: The type of transport (metro, train or tramway)
        enum: 
          - metro
          - train
          - tramway
    responses:
      200:
        description: OK
      400:
        description: Bad Request
    """

    if type not in TRANSPORT_TYPES:
        return jsonify({'message': 'Invalid transport type. Please choose among metro, train, tramway.'}), 400
    
    return jsonify({'message': f'Traffic of {type} from RATP network'})


@app.route('/traffic/<string:type>/<string:code>', methods=['GET'])
def get_traffic_by_line(type, code):
    """
    Get traffic of a specific line from the RATP network.
    ---
    parameters:
      - name: type
        in: path
        type: string
        required: true
        description: The type of transport (metro, train or tramway)
        enum: 
          - metro
          - train
          - tramway
      - name: code
        in: path
        type: string
        required: true
        description: The code of transport line
    responses:
      200:
        description: OK
      400:
        description: Bad Request
    """

    if type not in TRANSPORT_TYPES:
        return jsonify({'message': 'Invalid transport type. Please choose among metro, train, tramway.'}), 400
    

    return jsonify({'message': f'Traffic of {type} line with code {code}'})