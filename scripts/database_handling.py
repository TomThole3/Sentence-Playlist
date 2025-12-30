# -*- coding: utf-8 -*-

import os
import sqlite3

class DataBaseHandling:
    """
    SQLite database cache for storing resolved track IDs
    """

    def __init__(self, path):
        """
        :param path: Directory for the database file
        """
        self.database_path = os.path.join(path, "song_ids.db")
        self.conn = sqlite3.connect(self.database_path)
        self.initialize_table()

    def initialize_table(self):
        """
        Creates the song_ids database if it does not yet exist
        """
        with self.conn:
            self.conn.execute("""CREATE TABLE IF NOT EXISTS song_ids (song TEXT PRIMARY KEY,track_id TEXT)""")

    def check_database(self, word):
        """
        Looks up a word or phrase in the cache

        :param word: Word or phrase
        :return: Spotify track ID or None
        """
        cur = self.conn.execute("SELECT track_id FROM song_ids WHERE song = ?", (word,))
        row = cur.fetchone()
        return row[0] if row else None

    def add_database(self, word, track_id):
        """
        Stores a word and its associated track ID

        :param word: Word or phrase
        :param track_id: Spotify track ID
        """
        with self.conn:
            self.conn.execute("INSERT OR REPLACE INTO song_ids (song, track_id) VALUES (?, ?)", (word, track_id))

    def close(self):
        """
        Closes the database connection
        """
        self.conn.close()