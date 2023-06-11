from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
import requests
from transmission_rpc import Client
from threading import Thread
import time, sys, os
from datetime import timedelta

transmisson_host = os.environ.get('TR_HOST', 'localhost')
transmission_port = os.environ.get('TR_PORT', 9091)
transmisson_username = os.environ.get('TR_USER', None)
transmisson_password = os.environ.get('TR_PASS', None)
torrent_api_url = os.environ.get('TORRENT_API_URL', 'http://localhost:8080/api/v1/search')


tc = Client(host=transmisson_host, port=transmission_port, username=transmisson_username, password=transmisson_password)

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('q')
        response = requests.get(f'{torrent_api_url}?site=tgx&query={query}')
        results = response.json()
        print("[DEBUG]", results)
        if 'error' in results:
            return render_template('search.html', error=results.get('error'))
        results = results.get('data')
        results.sort(key=lambda r: r['size'], reverse=True)
        results = results[:15]
        return render_template('search.html', results=results)
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    magnet = request.form.get('magnet')
    if magnet:
        tc.add_torrent(magnet)
        flash('Torrent scheduled for download', 'success')
    else:
        flash('No magnet link provided', 'error')
    return redirect(url_for('home'))

socketio = SocketIO(app, cors_allowed_origins="*")  # Remove cors_allowed_origins="*" for production

def get_all_torrents():
    torrents = tc.get_torrents()
    return torrents


def background_thread():
    while True:
        socketio.sleep(5)  # Wait for 5 seconds
        torrents = get_all_torrents()
        socketio.emit('downloads', [{'id': t.id, 
                                     'name': t.name, 
                                     'total_size': t.total_size, 
                                     'downloaded': t.downloaded_ever, 
                                     'progress': t.progress, 
                                     'status': t.status.value, 
                                     'added_date': t.added_date.timestamp(), 
                                     'eta': str(timedelta(seconds=t.eta)) if t.eta != -1 and t.eta else 'unknown',} for t in torrents])

@socketio.on('connect')
def connect():
    socketio.emit('downloads', [{'id': t.id, 
                                     'name': t.name, 
                                     'total_size': t.total_size, 
                                     'downloaded': t.downloaded_ever, 
                                     'progress': t.progress, 
                                     'status': t.status.value, 
                                     'added_date': t.added_date.timestamp(), 
                                     'eta': str(timedelta(seconds=t.eta)) if t.eta != -1 and t.eta else 'unknown',} for t in get_all_torrents()])

    Thread(target=background_thread).start()

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

@app.route('/delete', methods=['POST'])
def delete_torrent():
    torrent_id = request.form.get('torrent_id')
    if torrent_id:
        tc.remove_torrent(int(torrent_id), delete_data=True)
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error'}), 400

@app.route('/pause/<int:id>', methods=['POST'])
def pause_torrent(id):
    tc.stop_torrent(id)
    return jsonify({'status': 'success'})

@app.route('/resume/<int:id>', methods=['POST'])
def resume_torrent(id):
    tc.start_torrent(id)
    return jsonify({'status': 'success'})



if __name__ == '__main__':
    print("[DEBUG] Starting server...")
    print("[DEBUG] Listening on port 8443")
    print("[DEBUG] Press Ctrl+C to exit")
    print("[DEBUG] Visit http://localhost:8443")
    print("[DEBUG]", get_all_torrents())
    socketio.run(app,debug=True, port=8443, host='0.0.0.0')
