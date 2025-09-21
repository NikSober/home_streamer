
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('searchForm');
    const input = document.getElementById('searchInput');
    const resultsDiv = document.getElementById('results');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = encodeURIComponent(input.value.trim());
        resultsDiv.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div><br><em>Loading...</em></div>';
        try {
            const res = await fetch(`/torrents/${query}`);
            if (!res.ok) throw new Error('API error');
            const data = await res.json();
            if (!Array.isArray(data) || data.length === 0) {
                resultsDiv.innerHTML = '<div class="alert alert-warning">No results found.</div>';
                return;
            }
            resultsDiv.innerHTML = '';
            data.forEach(category => {
                category.forEach(item => {
                    const col = document.createElement('div');
                    col.className = 'col-md-6 col-lg-4';
                    const card = document.createElement('div');
                    card.className = 'card shadow-sm';
                    // Build card body using DOM methods
                    const cardBody = document.createElement('div');
                    cardBody.className = 'card-body';

                    // Title
                    const title = document.createElement('h5');
                    title.className = 'card-title';
                    title.textContent = item.Name || 'Unknown';
                    cardBody.appendChild(title);

                    // Size
                    const sizeP = document.createElement('p');
                    sizeP.className = 'card-text mb-1';
                    sizeP.innerHTML = `<strong>Size:</strong> ${item.Size || 'N/A'}`;
                    cardBody.appendChild(sizeP);

                    // Source link
                    const sourceP = document.createElement('p');
                    sourceP.className = 'card-text mb-1';
                    const sourceA = document.createElement('a');
                    sourceA.href = item.Url;
                    sourceA.target = '_blank';
                    sourceA.textContent = 'Source';
                    sourceP.appendChild(sourceA);
                    cardBody.appendChild(sourceP);

                    // Torrent link
                    const torrentP = document.createElement('p');
                    torrentP.className = 'card-text mb-1';
                    const torrentA = document.createElement('a');
                    torrentA.href = item.Torrent;
                    torrentA.target = '_blank';
                    torrentA.textContent = 'Torrent';
                    torrentP.appendChild(torrentA);
                    cardBody.appendChild(torrentP);

                    // Magnet link
                    const magnetP = document.createElement('p');
                    magnetP.className = 'card-text mb-1';
                    const magnetA = document.createElement('a');
                    magnetA.href = item.Magnet;
                    magnetA.target = '_blank';
                    magnetA.textContent = 'Magnet';
                    magnetP.appendChild(magnetA);
                    cardBody.appendChild(magnetP);

                    // Download button
                    const downloadBtn = document.createElement('button');
                    downloadBtn.className = 'btn btn-success w-100';
                    downloadBtn.textContent = 'Download to server';
                    downloadBtn.onclick = function() {
                        send_download(
                            item.Name,
                            item.Magnet,
                            item.Url
                        );
                    };
                    cardBody.appendChild(downloadBtn);

                    card.appendChild(cardBody);
                    col.appendChild(card);
                    resultsDiv.appendChild(col);
                });
            });
        } catch (err) {
            resultsDiv.innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
        }
    });
});

function send_download(torrent, magnet, torrentUrl) {
    let torrent_url = magnet || torrentUrl;
    console.log(torrent_url);
    console.log(torrent);

    fetch('/download-content', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "torrent_name": torrent, "torrent_url": torrent_url})
    })
    .then(res => {
        if (!res.ok) throw new Error('Download failed');
        return res.json();
    })
    .catch(err => {
        alert('Error: ' + err.message);
        console.error(err);
    });
}
function get_tv_shows() {
    fetch('/list-tv-shows', {
        method: 'GET',
    })
    .then(res => {
        if (!res.ok) throw new Error('API error');
        return res.json();
    })
    .then(data => {
        console.log('TV Shows:', data);
    })
    .catch(err => {
        console.error('Error fetching TV shows:', err);
    });
}
function get_movies() {
    fetch('/list-movies', {
        method: 'GET',
    })
    .then(res => {
        if (!res.ok) throw new Error('API error');
        return res.json();
    })
    .then(data => {
        console.log('Movies:', data);
    })
    .catch(err => {
        console.error('Error fetching movies:', err);
    });
}
