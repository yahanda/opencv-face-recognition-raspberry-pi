
import json
import os
import io

# Imports for the REST API
from flask import Flask, request, jsonify

# Imports for image procesing
from PIL import Image

# Imports for prediction
from predict import initialize, predict_image

app = Flask(__name__)

# 4MB Max image size limit
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024 

# Default route just shows simple text
@app.route('/')
def index():
    return 'opencv face recognition model host harness'

@app.route('/image', methods=['POST'])
def predict_image_handler():
    try:
        imageData = None
        if ('imageData' in request.files):
            imageData = request.files['imageData']
        elif ('imageData' in request.form):
            imageData = request.form['imageData']
        else:
            imageData = io.BytesIO(request.get_data())

        img = Image.open(imageData)
        results = predict_image(img)
        return jsonify(results)
    except Exception as e:
        print('EXCEPTION:', str(e))
        return 'Error processing image', 500

if __name__ == '__main__':
    initialize()

    # Run the server
    app.run(host='0.0.0.0', port=80)
