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

temp_root = tempfile.gettempdir()

@app.route('/status/<request_id>', methods=['GET'])
def status(request_id):
    log.info(f"Checking request: {request_id}")
    target_dir = f"{temp_root}/{request_id}"
    if not os.path.isdir(target_dir):
        abort(404)

    files = os.listdir(target_dir)
    if not 'SUCCESS' in files:
        return jsonify({'request_id': request_id, 'status': 'in_progress'})

    files.remove('SUCCESS')
    target_dir = f"{target_dir}/{files[0]}"
    file_paths = []
    for f in os.listdir(target_dir):
        file_paths.append(f"{target_dir}/{f}")
    
    return jsonify({'request_id': request_id, 'status': 'success', 'output_files': file_paths})

@app.route('/invoke', methods=['POST'])
def invoke():
    if not request.json or 'original_file' not in request.json:
        abort(400)
  
    payload = request.json 
    original_file = payload['original_file']

    separator_type = 'spleeter:2stems'
    if 'split_type' in payload:
        separator_type = payload['split_type']

    if not separator_type in ['spleeter:2stems', 'spleeter:4stems', 'spleeter:5stems']:
        abort(400)
  
    request_id = str(uuid.uuid4())
    target_dir = f"{temp_root}/{request_id}" 
    os.mkdir(target_dir)   

    zmq_message = { 'source_file': original_file, 'split_type': separator_type, 'request_id': request_id, 'target_dir': target_dir }
    zmq_socket.send_json(zmq_message)

    return jsonify({'request_id': request_id})


if __name__ == '__main__':
    log.info("Starting REST API...")
    app.run(host='127.0.0.1', port=8080, debug=True)

