from django import forms
from django.core import validators
#from modules.h2hClass import *
#from django.forms import NumberInput
import requests

def checkH2HLeague(value):
    url = 'https://fantasy.premierleague.com/api/leagues-h2h/' +str(value)+ '/standings/'
    r = requests.get(url)
    json = r.json()
    print(json)
    try:
        y=json['standings']['results']
    except:
        raise forms.ValidationError("Error obtaining data, are you sure this is a valid head-to-head league number?")

class supplyLeagueNumber(forms.Form):
    league_number = forms.IntegerField(
                                      label="Enter League Number:",validators =[checkH2HLeague],
                                      widget=forms.NumberInput(attrs={'placeholder': 'e.g. 783464',"class": 'league_number_input',})
                                      )

    #error_css_class = 'validationError'
