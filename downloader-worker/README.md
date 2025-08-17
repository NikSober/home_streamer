# Downloader Worker

A simple web-based torrent downloader worker. It exposes a REST API using Flask to submit torrent URLs or magnet links for download. The worker uses a single shared [libtorrent](https://www.libtorrent.org/) session to manage multiple concurrent downloads efficiently.

## Features

- Accepts JSON requests to download torrents or magnet links.
- Restricts downloads to safe file types (video, audio, ISO).
- Tracks download status: in progress, completed, or failed.
- Health check endpoint.
- Container-ready (see Dockerfile).

## API

### Health Check

**Endpoint:** `GET /health`

Returns the status of the worker, including counts of active, completed, and failed downloads.

---

### Start a Download

**Endpoint:** `POST /download`

- Accepts a JSON body with `torrent_url` (direct `.torrent` file URL or magnet link).
- Returns a `download_id` to check the status.

---

### Check Download Status

**Endpoint:** `GET /status/<download_id>`

Returns the status for the given download.

---

## Usage

### Requirements

- Python 3.9+
- [libtorrent](https://pypi.org/project/libtorrent/) (see Dockerfile for system dependencies)
- Python dependencies in `requirements.txt`

### Running Locally

1. Install system dependencies for libtorrent (see Dockerfile for details).
2. Install Python dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. Start the server:

    ```sh
    python app.py
    ```

### Running with Docker

Build and run the container:

```sh
docker build -t downloader-worker .
docker run -p 8008:8008 -p 6881:6881 downloader-worker
```