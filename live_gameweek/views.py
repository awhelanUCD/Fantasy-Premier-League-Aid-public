from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from json import dumps
from .forms import supplyLeagueNumber

import requests
import pandas as pd
from modules.h2hClass import h2hLeague_live
from config.global_definitions import *

from live_gameweek.forms import supplyLeagueNumber

def live_gameweek_form(request):

    form = supplyLeagueNumber()

    if request.method == 'POST':

        # Create a form instance and populate it with data from the request:
        form = supplyLeagueNumber(request.POST)

        # Check if the form is valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required (here we just write it to the model leagueNumber field)
            leagueNumber = form.cleaned_data['league_number']


            gameweek=CURRENT_GAMEWEEK
            # If gameweek has concluded but a new gameweek has not yet started
            # we use the gameweek that has concluded
            if GAMEWEEK_ONGOING==False:
                gameweek=gameweek-1

            myLeague=h2hLeague_live(leagueNumber, gameweek, GAMEWEEK_ONGOING) #783464
            standings_df=myLeague.getCurrentStandings()
            fixtures_df_slim=myLeague.getFixtures()
            teamInfo_list=myLeague.updateFixtureResults(fixtures_df_slim)
            live_standings_df=standings_df.copy()

            myLeague.updateLiveTable(live_standings_df,standings_df,fixtures_df_slim)

            slim_live_standings_df=live_standings_df[['last_rank','rank','player_name','matches_played', 'matches_won',
                                                      'matches_drawn', 'matches_lost','total', 'points_for','wld_list',
                                                       'points_list']]
            sorted_df=slim_live_standings_df.sort_values(by=['total','points_for'], ascending=False)
            sorted_df=sorted_df.reset_index(drop=True)
            sorted_df=sorted_df.rename(columns={'rank':'Old Rank'})
            sorted_df.index.name = 'Rank'
            myLeague.createChangeList(sorted_df)
            JSON_Table=sorted_df.to_json(force_ascii = False,orient="table")

            context={
                     'league_Number':leagueNumber,
                     'fixtureData':fixtures_df_slim.to_json(force_ascii = False,orient="table"),
                     'leagueData':JSON_Table,'team_info':teamInfo_list.to_json(force_ascii = False,orient="table"),
                     'gamweek_ongoing':GAMEWEEK_ONGOING,
                     'current_gameweek': gameweek
                     }

            # return an new view
            return render(request, 'live_gameweek/live_gameweek.html', context)

        else:
            form = supplyLeagueNumber(request.POST)

    context = {'form': form,}

    return render(request, 'live_gameweek/live_gameweek_form.html', context)
