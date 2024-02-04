from flask import Flask, request, abort, jsonify

import logging
import os
import tempfile
import uuid
import zmq

app = Flask(__name__)

logging.basicConfig()
log = logging.getLogger("soundpicker-api")
log.setLevel(logging.INFO)

log.info("Initializing message publisher...")
global zmq_context
zmq_context = zmq.Context()
zmq_socket = zmq_context.socket(zmq.PUSH)
zmq_socket.connect("tcp://127.0.0.1:5555")
log.info("Message publisher ready")

input_dir = '/Users/okuklina/soundpicker_files/input'
output_dir = '/Users/okuklina/soundpicker_files/artifacts'
artifact_base_url = "http://127.0.0.1:8888/artifacts"

@app.route('/status/<request_id>', methods=['GET'])
def status(request_id):
    log.info(f"Checking request: {request_id}")
    target_dir = os.path.join(output_dir, request_id)
    if not os.path.isdir(target_dir):
        abort(404)

    files = os.listdir(target_dir)
    if not 'SUCCESS' in files:
        return jsonify({'request_id': request_id, 'status': 'in_progress'})

    files.remove('SUCCESS')
    target_dir = os.path.join(target_dir, files[0])
    file_urls = []
    for f in os.listdir(target_dir):
        file_urls.append(f"{artifact_base_url}/{request_id}/{files[0]}/{f}")
    
    return jsonify({'request_id': request_id, 'status': 'success', 'output_artifacts': file_urls})


@app.route('/invoke', methods=['POST'])
def invoke():
    if not request.json or 'source_id' not in request.json:
        abort(400)
  
    payload = request.json 
    source_dir = os.path.join(input_dir, payload['source_id'])
    if not os.path.isdir(source_dir):
        abort(404)

    source_file = os.listdir(source_dir)[0]

    separator_type = 'spleeter:2stems'
    if 'split_type' in payload:
        separator_type = payload['split_type']

    if not separator_type in ['spleeter:2stems', 'spleeter:4stems', 'spleeter:5stems']:
        abort(400)
  
    request_id = str(uuid.uuid4())
    target_dir = os.path.join(output_dir, request_id)
    os.mkdir(target_dir)   

    zmq_message = { 'source_file': os.path.join(source_dir, source_file), 'split_type': separator_type, 'request_id': request_id, 'target_dir': target_dir }
    zmq_socket.send_json(zmq_message)

    return jsonify({'request_id': request_id})


@app.route('/upload', methods=['POST'])
def upload():
    if not 'source_file' in request.files:
       abort(400)
    f = request.files['source_file']

    file_id = str(uuid.uuid4())
    target_dir = os.path.join(input_dir, file_id)
    os.mkdir(target_dir)

    filepath = os.path.join(target_dir, f.filename)
    log.info(f"Saving to {filepath}")
    f.save(filepath)
    return jsonify({'source_id': file_id})


if __name__ == '__main__':
    log.info("Starting REST API...")
    app.run(host='127.0.0.1', port=8080, debug=True)

