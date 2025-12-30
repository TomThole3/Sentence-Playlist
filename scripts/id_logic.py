# -*- coding: utf-8 -*-

class IDLogic:
    """
    Handles the logic for converting the sentence into Spotify track IDs
    """
    
    def __init__(self, io, db, api_interactions):
        """
        :param io: InputOutput instance
        :param db: DataBaseHandling instance
        :param api_interactions: APIInteractions instance
        """
        self.io = io
        self.db = db
        self.api_interactions = api_interactions
    
    def manage_ids(self, sentence, token, sequence):
        """
        Breaks a sentence into word sequences and resolves it to
        a Spotify track ID

        :param sentence: Input sentence
        :param token: Spotify access token
        :param sequence: Maximum number of words per lookup
        :return: List of Spotify track IDs
        """
        ids = []
        sentence = sentence.split(" ")
        while sentence:
            sequence = min(sequence, len(sentence))
            for i in reversed(range(sequence)):
                lookup = ' '.join(sentence[:i+1])
                id_ = self.collect_id(lookup, token)
                if id_ is None and i == 0:
                    word = self.io.word_not_found(lookup)
                    if '/' in word:
                        ids.append(word.split('/')[-1].split('?')[0])
                        sentence = sentence[1:]
                    else: 
                        sentence[0] = word
                    break
                elif id_ is not None:
                    ids.append(id_)
                    sentence = sentence[i+1:]
                    break
        return ids
    
    def collect_id(self, word, token):
        """
        Retrieves a track ID for a word or phrase using the database or
        else the Spotify API search
        
        :param word: Word or phrase to search for
        :param token: Spotify access token
        :return: Spotify track ID or None
        """
        max_iterations = 20
        check = self.db.check_database(word)
        if check is not None:
            return check
        for i in range(max_iterations):
            id_ = self.api_interactions.search_song(word, i, token)
            if not id_ is None:
                self.db.add_database(word, id_)
                return id_
        return None