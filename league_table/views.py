from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from league_table.forms import supplyLeagueNumber

from json import dumps

import requests
import pandas as pd
from modules.h2hClass import h2hLeague
from modules.classicLeagueClass import classicLeague
from config.global_definitions import*
from modules.checkLeagueType import checkLeagueType


def league_table(request):
  context = {}

  return render(request, "league_table/league_table.html", context)


def league_table_submit(request):

     form = supplyLeagueNumber()

     if request.method == 'POST':

         # Create a form instance and populate it with data from the request (binding):
         form = supplyLeagueNumber(request.POST)

         # Check if the form is valid:
         if form.is_valid():
             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
             leagueNumber = form.cleaned_data['league_number']

             league_type=checkLeagueType(leagueNumber)

             if league_type == "head2head":
                 myLeague=h2hLeague(leagueNumber,CURRENT_GAMEWEEK) #783464
                 standings_df=myLeague.getCurrentStandings()
                 myLeague.createForm(standings_df)
                 myLeague.createPercentileColumn(standings_df)
                 slim_standings_df=standings_df[['rank','player_name','matches_played', 'matches_won', 'matches_drawn', 'matches_lost','total', 'points_for','form','percentile']]
                 print(slim_standings_df)

             elif league_type == "classic":
                myLeague=classicLeague(leagueNumber,CURRENT_GAMEWEEK)
                standings_df=myLeague.getCurrentStandings()
                myLeague.createPercentileColumn(standings_df)
                myLeague.createForm(standings_df)
                slim_standings_df=standings_df[['rank','player_name','event_total','total','five_game_average','percentile']]
                print(slim_standings_df)

             context={
                       'league_Number':leagueNumber,
                       'leagueData':slim_standings_df.to_json(force_ascii = False,orient="table"),
                       "league_type":league_type
                     }

             return render(request, 'league_table/league_table.html', context)
         else:
            form = supplyLeagueNumber(request.POST)


     context = {'form': form,}

     return render(request, 'league_table/league_table_form.html', context)
