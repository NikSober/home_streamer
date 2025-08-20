from flask import Flask, jsonify, render_template, request
import requests
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to HomeStreamer!"})

@app.route('/search')
def search():
    print("neki")
    return render_template('search.html')
@app.route('/download-content', methods=['POST'])
def reroute():
    data = request.json
    print(data)
    response = requests.post('http://downloader-worker:8008/download-content', json=data)
    return jsonify(response.json()), response.status_code
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)