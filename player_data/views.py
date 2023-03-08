from django.shortcuts import render
import requests
import pandas as pd

def player_data(request):#
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    r = requests.get(url)
    json = r.json()
    elements_df = pd.DataFrame(json['elements'])

    playerData = elements_df[[
                             'web_name',
                             'team',
                             'element_type',
                             'starts',
                             'assists',
                             'total_points',
                             'points_per_game',
                             'goals_scored',
                             'expected_goals',
                             'expected_assists',
                             'clean_sheets',
                             'goals_conceded',
                             'expected_goals_conceded',
                             'expected_goal_involvements',
                              'expected_assists_per_90',
                             'expected_goal_involvements_per_90',
                             'expected_goals_conceded_per_90',
                             'expected_goals_per_90',
                             'starts_per_90'
                             ]]
    context = {
               'playerData':playerData.to_json(force_ascii = False,orient="table"),
              }

    return render(request, 'player_data/player_data.html', context)
# Create your views here.

def toggle_test(request):#
    context = {

              }
    return render(request, 'player_data/toggle_test.html', context)
