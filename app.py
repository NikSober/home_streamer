from flask import Flask, jsonify, render_template, request
import requests
app = Flask(__name__)

@app.route('/')
def home():
    return search()

@app.route('/search')
def search():
    return render_template('search.html')
@app.route('/download-content', methods=['POST'])
def reroute():
    data = request.get_json()
    response = requests.post('http://downloader-worker:8008/download-content', json=data)
    return jsonify(response.json()), response.status_code

@app.route('/list-tv-shows',methods=['GET'])
def list_shows():
    response = requests.get('http://downloader-worker:8008/list-tv-shows')
    return response.json(), response.status_code

@app.route('/list-movies',methods=['GET'])
def list_movies():
    response = requests.get('http://downloader-worker:8008/list-movies')
    return response.json(), response.status_code
@app.route("/torrents/<query>")
def fetch_torrents(query):
    response = requests.get(f'http://finder:8080/api/all/{query}')
    return response.json(), response.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)