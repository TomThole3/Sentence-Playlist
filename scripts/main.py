# -*- coding: utf-8 -*-
"""
This script converts an input sentence into a Spotify playlist by matching words or
word sequences to Spotify track titles. This process involves authentication, Spotify API
communication, caching track IDs in a SQLite database, and interactive user input
when matches cannot be found automatically
"""

from app import SentencePlaylist
from input_output import InputOutput
from id_logic import IDLogic
from spotify_api import TokenHandling
from spotify_api import APIInteractions
from database_handling import DataBaseHandling
from pathlib import Path

def main():
    cwd = Path.cwd()
    path = cwd.parents[0]
    
    api_interactions = APIInteractions()
    token_handling = TokenHandling(path, api_interactions)
    io = InputOutput()
    db = DataBaseHandling(path)
    id_logic = IDLogic(io, db, api_interactions)

    app = SentencePlaylist(token_handling, io, id_logic, api_interactions, db)
    app.run() 


if __name__ == "__main__":
    main()