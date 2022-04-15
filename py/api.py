from flask import Flask, request, jsonify, json

app = Flask(__name__)  # name of file is the app name

@app.route('/job', methods=['POST'])
def job():
    data = json.loads(request.data)
    return data

if __name__ == "__main__":
    app.run(host='0.0.0.0')
