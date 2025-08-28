import libtorrent as lt
import time
import os
import sys
import urllib.request
class Downloader:
# Create a single session at module level
    def __init__(self):
        self.SESSION = lt.session({'listen_interfaces': '0.0.0.0:6881'})

    def is_allowed_torrent_format(self,torrent_path: str) -> bool:
            """
            Checks if the torrent file contains only allowed formats.
            Allowed: video, audio, ISO files. Forbids executables and other types.

            Args:
                torrent_path (str): Path to the .torrent file.

            Returns:
                bool: True if all files are allowed, False otherwise.
            """
            allowed_exts = {
                ".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm", ".mp3", ".aac", ".flac",
                ".wav", ".ogg", ".m4a", ".iso", ".jpg", ".jpeg", ".png", ".gif",".14-x86_64-checksum","txt"
            }
            forbidden_exts = {
                ".exe", ".bat", ".sh", ".msi", ".apk", ".com", ".scr", ".cmd", ".js", ".jar", ".ps1"
            }

            try:
                info = lt.torrent_info(torrent_path)
                for f in info.files():
                    ext = os.path.splitext(f.path)[1].lower()
                    if ext in forbidden_exts:
                        print(ext, "is a forbidden format.")
                        return False
                    if ext not in allowed_exts:
                        print(ext, "is a not allowed format.")
                        return False
                return True
            except Exception as e:
                print(f"Error checking torrent format: {e}")
                return False

    def download_torrent(self, torrent_path: str, download_dir: str = "/home_streamer/torrents", is_tv_show: bool = False):
        """
        Download a torrent using a shared libtorrent session.
        Handles both .torrent files and magnet links correctly.
        """
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # If torrent_path is a URL, download the file first
        if torrent_path.startswith("http://") or torrent_path.startswith("https://"):
            torrent_files_dir = "/home_streamer/torrent_files"
            if not os.path.exists(torrent_files_dir):
                os.makedirs(torrent_files_dir)
            local_filename = os.path.join(
                torrent_files_dir, os.path.basename(torrent_path.split("?")[0])
            )
            urllib.request.urlretrieve(torrent_path, local_filename)
            torrent_path = local_filename

        ses = self.SESSION

        if torrent_path.startswith("magnet:"):
            params = {
                'save_path': download_dir,
            }
            print("Starting download from magnet link")
            handle = lt.add_magnet_uri(ses, torrent_path, params)

            # Wait for metadata
            print("Waiting for metadata...")
            while not handle.has_metadata():
                for alert in ses.pop_alerts():
                    if alert.category() & lt.alert.category_t.error_notification:
                        print("[ERROR]", alert)
                time.sleep(1)
            print("Metadata received!")
        else:
            if not self.is_allowed_torrent_format(torrent_path=torrent_path):
                print("Torrent file contains forbidden formats.")
                return None
            info = lt.torrent_info(torrent_path)
            handle = ses.add_torrent({'ti': info, 'save_path': download_dir})

        print("Starting download:", handle.status().name)

        while not handle.status().is_seeding:
            s = handle.status()
            print(
                f"\r{s.progress * 100:.2f}% complete "
                f"(down: {s.download_rate / 1000:.1f} kB/s "
                f"up: {s.upload_rate / 1000:.1f} kB/s "
                f"peers: {s.num_peers}) {s.state}", 
                end=" "
            )

            # check alerts (errors, etc.)
            for alert in ses.pop_alerts():
                if alert.category() & lt.alert.category_t.error_notification:
                    print("\n[ERROR]", alert)

            sys.stdout.flush()
            time.sleep(1)

        print(f"\n{handle.status().name} complete!")
        # Remove torrent to prevent seeding
        ses.remove_torrent(handle)
        print("Torrent removed from session to prevent seeding.")
    print("Torrent removed from session to prevent seeding.")


