"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls
Website is: http://deckofcardsapi.com

Instructions:

- Review instructions in I-Learn.
n1kisstd7moh

"""

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results

    
    # https://realpython.com/python-requests/
    pass

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        print('Reshuffle Deck')
        # TODO - add call to reshuffle
        requests.get("https://deckofcardsapi.com/api/deck/n1kisstd7moh/shuffle/")
        


    def draw_card(self):
        # TODO add call to get a card
        card = requests.get('https://deckofcardsapi.com/api/deck/n1kisstd7moh/draw/?count=1')
        card = card.content
        cardpayload = json.loads(card)
        value = [card["value"] for card in cardpayload["cards"]]
        val = value[0]
        suit = [card["suit"] for card in cardpayload["cards"]]
        sweet = suit[0]
        return val, sweet

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = 'n1kisstd7moh'
    
    # Testing Code >>>>>
    deck = Deck(deck_id)
    
    for i in range(55):
        card = deck.draw_endless()
        print(f'card {i + 1}: {card[0]} : {card[1]}', flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<

