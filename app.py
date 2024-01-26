from flask import Flask, request, abort, jsonify
from spleeter.separator import Separator
import os, tempfile

temp_dir = tempfile.gettempdir()
app = Flask(__name__)


@app.route('/invoke', methods=['POST'])
def invoke():
    if not request.json or 'original_file' not in request.json:
        abort(400)
   
    original_file = request.json['original_file']
    print(f"Processing {original_file}")

    separator = Separator('spleeter:2stems')
    separator.separate_to_file(original_file, temp_dir)

    original_file_short_name = original_file.split("/")[-1].split(".")[0]
    output_dir = f"{temp_dir}/{original_file_short_name}"
    files = os.listdir(output_dir)
    file_paths = []
    for f in files:
        file_paths.append(f"{output_dir}/{f}")
   
    return jsonify({'status': 'success', 'output_files': file_paths})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

