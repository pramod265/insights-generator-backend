import os
from flask import Flask, request, abort, jsonify, send_from_directory
import datetime
import pandas as pd
from pandas_profiling import ProfileReport


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIRECTORY = "/uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


# app = Flask(__name__, static_folder="build/static", template_folder="build")
app = Flask(__name__)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    header['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST, DELETE, PUT'
    return response

@app.route("/")
def hello():
    return "Hello"

    # return render_template('index.html')

@app.route("/time")
def get_current_time():
    return {"time": datetime.datetime.now()}


@app.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@app.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@app.route("/files/<filename>", methods=["POST"])
def post_file(filename):
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)
    
    # Return 201 CREATED
    return "", 201


@app.route("/generate_report", methods=["POST"])
def generate_report():
    file = request.files['file']
    data = pd.read_csv(file)

    profile = ProfileReport(data, title='Report')

    profile.to_file("uploaded_files/your_report.html")

    response = send_from_directory(directory='uploaded_files', filename='your_report.html')
    response.headers['my-custom-header'] = 'my-custom-status-0'
    return response

print('Starting Flask!')

app.debug=True
app.run(host='0.0.0.0')
