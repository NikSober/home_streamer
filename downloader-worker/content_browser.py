import os
import json

class ContentBrowser:
    HOME_DIR = "/home_streamer/torrents"
    TV_SHOWS_DIR = os.path.join(HOME_DIR, "TV Shows")
    MOVIES_DIR = os.path.join(HOME_DIR, "Movies")

    @staticmethod
    def list_tv_shows():
        try:
            return str(os.listdir(ContentBrowser.TV_SHOWS_DIR))
        except Exception as e:
            print(f"Error listing TV shows: {e}")
            return []

    @staticmethod
    def list_movies():
        try:
            return str(os.listdir(ContentBrowser.MOVIES_DIR))   
        except Exception as e:
            print(f"Error listing movies: {e}")
            return []
    @staticmethod
    def list_all_content():
        return {
            "TV Shows": ContentBrowser.list_tv_shows(),
            "Movies": ContentBrowser.list_movies()
        }