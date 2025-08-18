from flask import Flask, request, jsonify
from threading import Thread
from torrent_downloader import Downloader
import uuid
import socket

app = Flask(__name__)
download_status = {}
dwn = Downloader()
def download_wrapper(torrent_url, download_id):
    try:
        dwn.download_torrent(torrent_url)
        download_status[download_id] = 'completed'
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
    Thread(target=download_wrapper, args=(torrent_url, download_id)).start()
    return jsonify({'status': 'Download started', 'download_id': download_id}), 202

@app.route('/download-status/<download_id>', methods=['GET'])
def get_download_status(download_id):
    status = download_status.get(download_id)
    if status is None:
        return jsonify({'error': 'Invalid download_id'}), 404
    return jsonify({'download_id': download_id, 'status': status})

if __name__ == '__main__':
    app.run(debug=True,threaded=True,port=8008,host='0.0.0.0')