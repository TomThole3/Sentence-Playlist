# -*- coding: utf-8 -*-



class SentencePlaylist:
    """
    High-level controller class that coordinates the entire process
    """

    def __init__(self, token_handling, io, id_logic, api_interactions, db):
        """
        :param token_handling: TokenHandling instance
        :param io: InputOutput instance
        :param id_logic: IDLogic instance
        :param api_interactions: APIInteractions instance
        :param db: DataBaseHandling instance
        """
        self.token_handling = token_handling
        self.io = io
        self.id_logic = id_logic
        self.api_interactions = api_interactions
        self.db = db
    
    def run(self):
        """
        Executes the full playlist creation process
        """
        access_token = self.token_handling.get_access_token()
        sentence, sequence, title = self.io.get_information()
        ids = self.id_logic.manage_ids(sentence, access_token, sequence)
        self.api_interactions.create_playlist(title, ids, access_token)
        self.db.close()

