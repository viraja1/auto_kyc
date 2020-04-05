import os
import json


from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, jsonify
import boto3

app = Flask('auto_kyc')


SAGEMAKER_ENDPOINT = os.environ.get("SAGEMAKER_ENDPOINT")
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
AWS_REGION = os.environ.get("AWS_REGION")

runtime = boto3.client('runtime.sagemaker', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY,
                       region_name=AWS_REGION)

print('Check http://127.0.0.1:8080/')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/auto_kyc', methods=['POST'])
def auto_kyc():
    img = request.files['file'].read()
    payload = bytearray(img)
    response = runtime.invoke_endpoint(EndpointName=SAGEMAKER_ENDPOINT, ContentType='application/x-image',
                                       Body=payload)
    result = json.loads(response['Body'].read().decode('utf-8'))
    print(result)
    return jsonify(result)


if __name__ == '__main__':
    http_server = WSGIServer(('', 8080), app)
    http_server.serve_forever()
