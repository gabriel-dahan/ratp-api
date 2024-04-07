from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)

app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "RATP API",
    "version": "1.0",
    "description": "A REST API for the RATP - Iledefrance mobilités",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
}

swagger = Swagger(app)

TRANSPORT_TYPES = ['metro', 'train', 'tramway', 'bus']

@app.route('/destinations/<string:type>/<string:code>', methods=['GET'])
def get_destinations(type, code):
    """
    Get destinations of a specific line from the RATP network.
    ---
    parameters:
      - name: type
        in: path
        type: string
        required: true
        description: The type of transport (metro, train, tramway, bus)
        enum: 
          - metro
          - train
          - tramway
          - bus
          
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
        return jsonify({'message': 'Invalid transport type. Please choose among metro, train, tramway, bus, noctiliens.'}), 400
    

    return jsonify({'message': f'Destinations for {type} line with code {code}'})



@app.route('/lines', methods=['GET'])
def get_all_lines():
    """
    Get all lines from the RATP network.
    ---
    responses:
      200:
        description: OK
    """

    return jsonify({'message': 'All lines from RATP network'})



@app.route('/lines/<string:type>', methods=['GET'])
def get_lines_by_type(type):
    """
    Get all lines of a specific type of transport from the RATP network.
    ---
    parameters:
      - name: type
        in: path
        type: string
        required: true
        description: The type of transport (metro, train, tramway, bus)
        enum: 
          - metro
          - train
          - tramway
          - bus
          
    responses:
      200:
        description: OK
      400:
        description: Bad Request
    """

    if type not in TRANSPORT_TYPES:
        return jsonify({'message': 'Invalid transport type. Please choose among metro, train, tramway, bus, noctiliens.'}), 400
    

    return jsonify({'message': f'All {type} lines from RATP network'})



@app.route('/lines/<string:type>/<string:code>', methods=['GET'])
def get_line_information(type, code):
    """
    Get information about a specific line from the RATP network.
    ---
    parameters:
      - name: type
        in: path
        type: string
        required: true
        description: The type of transport (metro, train, tramway, bus)
        enum: 
          - metro
          - train
          - tramway
          - bus
          
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
        return jsonify({'message': 'Invalid transport type. Please choose among metro, train, tramway, bus, noctiliens.'}), 400
    

    return jsonify({'message': f'Information about {type} line with code {code}'})



@app.route('/schedules/<string:type>/<string:code>/<string:station>/<string:way>', methods=['GET'])
def get_schedules(type, code, station, way):
    """
    Get schedules at a specific station on a specific line.
    ---
    parameters:
      - name: type
        in: path
        type: string
        required: true
        description: The type of transport (metro, train, tramway, bus)
        enum: 
          - metro
          - train
          - tramway
          - bus
          
      - name: code
        in: pathC'est cool ça rend bien, faudra que tu me 
          - A+R
    responses:
      200:
        description: OK
      400:
        description: Bad Request
    """

    if type not in TRANSPORT_TYPES:
        return jsonify({'message': 'Invalid transport type. Please choose among metro, train, tramway, bus, noctiliens.'}), 400

    return jsonify({'message': f'Schedules at {station} station on {type} line with code {code} and way {way}'})



@app.route('/stations/<string:type>/<string:code>', methods=['GET'])
def get_stations(type, code):
    """
    Get stations of a specific line from the RATP network.
    ---
    parameters:
      - name: type
        in: path
        type: string
        required: true
        description: The type of transport (metro, train, tramway, bus)
        enum: 
          - metro
          - train
          - tramway
          - bus
          
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
        return jsonify({'message': 'Invalid transport type. Please choose among metro, train, tramway, bus, noctiliens.'}), 400
    
    return jsonify({'message': f'Stations of {type} line with code {code}'})


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


if __name__ == '__main__':
    app.run(debug=True)