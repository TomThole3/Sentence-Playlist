# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 16:44:48 2025

@author: tthol
"""

import re

class InputOutput:
    """
    Handles all user input and prompts
    """
    
    def get_information(self): 
        """
        Prompts the user for playlist details

        :return: (sentence, sequence length, playlist title)
        """
        title = input("What should the title of the playlist be? ")
        sentence = input("What should the text in the playlist be? ")
        while True: 
            sequence = input("What should the maximum number of words in one title be? ")
            if sequence.isdigit():
                break
            print("Please input an integer")
        return sentence, int(sequence), title
    
    def word_not_found(self, word):
        """
        Handles missing tracks by prompting the user

        :param word: Word or phrase that could not be found
        :return: Replacement word or Spotify track URL
        """
        while True:
            response = input(f"Could not find {word}, replace it (r), insert id (i) or quit (q)? ")
            if response == 'r':
                new = input("What should the replacement word be? ")
                return new
            elif response == 'q':
                exit()
            elif response == 'i':
                while True:
                    id_ = input(f'what is the valid id for {word}? ')
                    if re.fullmatch(r'^https://open\.spotify\.com/track/[A-Za-z0-9]{22}\?si=[A-Za-z0-9]+$', id_):
                        break
                    print("Please enter a valid spotify link")
                return id_
            print("that is not a valid input")