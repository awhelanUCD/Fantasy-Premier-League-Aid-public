from django import forms
from django.core import validators
import requests

def checkH2HLeague(value):
    try:
        url = 'https://fantasy.premierleague.com/api/leagues-h2h/' +str(value)+ '/standings/'
        r = requests.get(url)
        json = r.json()
        y=json['standings']['results']

    except:
      try:
        url = 'https://fantasy.premierleague.com/api/leagues-classic/' +str(value)+ '/standings/'
        r = requests.get(url)
        json = r.json()
        standings_df = json['standings']['results']

      except:
        raise forms.ValidationError("Error obtaining data, are you sure this is a valid head-to-head or classic league number?")

class supplyLeagueNumber(forms.Form):
    league_number = forms.IntegerField(
                                      label="Enter League Number:", validators =[checkH2HLeague],
                                      widget=forms.NumberInput(attrs={'placeholder': 'e.g. 783464',"class": 'league_number_input',})
                                      )
