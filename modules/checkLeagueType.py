import requests
import json

def checkLeagueType(value):
    """
    Check whaat type of league a given league ID corresponds to

    :param value: the league id
    :type number: int

    :rtype: string defining the league type
    """

    try:
        url = 'https://fantasy.premierleague.com/api/leagues-h2h/' +str(value)+ '/standings/'
        r = requests.get(url)
        json = r.json()
        y=json['standings']['results']
        return "head2head"

    except:
      try:
        url = 'https://fantasy.premierleague.com/api/leagues-classic/' +str(value)+ '/standings/'
        r = requests.get(url)
        json = r.json()
        standings_df = json['standings']['results']
        return "classic"
      except:
        pass
