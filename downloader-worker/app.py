from flask import Flask, request, jsonify
from threading import Thread
from torrent_downloader import Downloader
import uuid
import socket
from content_browser import ContentBrowser
import subprocess

app = Flask(__name__)
download_status = {}
download_exit_message = {}
COMMAND = "filebot -rename \"/home_streamer/tmp\" --output \"/home_streamer/torrents\" --format \"{plex}\""
dwn = Downloader()
def download_wrapper(torrent_url, download_id):
    exit_status = ""
    try:
        exit_status = dwn.download_torrent(torrent_path=torrent_url, download_dir='/home_streamer/tmp')
        download_status[download_id] = 'completed'
        download_exit_message[download_id] = exit_status
        if exit_status == 0:
            subprocess.call(COMMAND, shell=True)


    except Exception as e:
        download_status[download_id] = f'failed: {str(e)}'

@app.route('/health', methods=['GET'])
def healthcheck():
    health = {
        'status': 'ok',
        'app': 'downloader-worker',
        'hostname': socket.gethostname(),
        'active_downloads': sum(1 for v in download_status.values() if v == 'in_progress'),
        'completed_downloads': sum(1 for v in download_status.values() if v == 'completed'),
        'failed_downloads': sum(1 for v in download_status.values() if v.startswith('failed')),
    }
    return jsonify(health), 200

@app.route('/download-content', methods=['POST'])
def download_content():
    data = request.get_json()
    if not data.get('torrent_name') or not data.get('torrent_url'):
        return jsonify({'error': 'Missing torrent name or URL'}), 400
    torrent_url = data['torrent_url']

    download_id = str(uuid.uuid4())
    download_status[download_id] = 'in_progress'
    download_exit_message[download_id] = ''

    Thread(target=download_wrapper, args=(torrent_url, download_id)).start()
    return jsonify({'status': 'Download started', 'download_id': download_id}), 202

@app.route('/download-status/<download_id>', methods=['GET'])
def get_download_status(download_id):
    status = download_status.get(download_id)
    if status is None:
        return jsonify({'error': 'Invalid download_id'}), 404
    return jsonify({'download_id': download_id, 'status': status})


@app.route('/list-tv-shows', methods=['GET'])
def list_tv_shows():
    shows = ContentBrowser.list_tv_shows()
    return jsonify(shows), 200

@app.route('/list-movies', methods=['GET'])
def list_movies():
    movies = ContentBrowser.list_movies()
    return jsonify(movies), 200

@app.route('/list-all-content', methods=['GET'])
def list_all_content():
    content = ContentBrowser.list_all_content()
    return jsonify(content), 200

if __name__ == '__main__':
    app.run(debug=True,threaded=True,port=8008,host='0.0.0.0')

