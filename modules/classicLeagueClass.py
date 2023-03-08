import requests
import pandas as pd
import json

from modules.sharedFunctions.sharedFunctions import  getTotalPlayers

pd.options.mode.chained_assignment = None

class classicLeague:

    def __init__(self,leagueNo,currentGameweek):
        self.leagueNo=leagueNo
        self.currentGameweek=currentGameweek

    def getCurrentStandings(self):

        """
        Return the current standings of given fpl classic league

        :return: current standings data object
        :rtype: pandas dataframe
        """

        url = 'https://fantasy.premierleague.com/api/leagues-classic/' +str(self.leagueNo)+ '/standings/'
        r = requests.get(url)
        json = r.json()
        standings_df = pd.DataFrame(json['standings']['results'])

        return standings_df

    def createPercentileColumn(self,df):

        """
        Adds a percentile column to a dataframe which holds the current standings

        :param df: the current standings dataframe
        :type df: pandas dataframe
        """

        # Get the total number of fpl platers
        totalPlayers=getTotalPlayers()

        # Empty list which will hold the percentile rank for each fpl player
        percentile_list=[]

        # Loop throgh entries and calculate percentile
        for entry in df.entry:
            try:
              url='https://fantasy.premierleague.com/api/entry/'+str(int(entry))+'/'
              r = requests.get(url)
              print(r)
              percentile = 100*(totalPlayers-r.json()['summary_overall_rank'])/totalPlayers
              print("percentile: ", percentile)
              percentile_list.append(percentile)
            except:
              percentile_list.append('-')

        # Add percentile column to standings dataframe
        df.insert(len(df.columns),"percentile",percentile_list)

    def createForm(self,standings_df):

        """
        Adds a form column to a dataframe which holds the current standings

        :param standings_df: the current standings dataframe
        :type standings_df: pandas dataframe
        """

        # Initialise list which will hold the 5 gameweek points average for each
        # fpl player
        avg_points_list=[]

       # Loop through each fpl player and create form
        for entry in standings_df['entry']:

            url='https://fantasy.premierleague.com/api/entry/'+str(entry)+'/history/'
            r = requests.get(url)
            json = r.json()
            player_history_df=pd.DataFrame(json['current'])
            print(player_history_df)

            n_Gameweeks=len(player_history_df.index)
            total_points=0
            for i in range(n_Gameweeks-1,n_Gameweeks-6,-1):
                total_points += player_history_df.iloc[i]['points']
            average_points=total_points/5
            avg_points_list.append(average_points)

        # Add form column to standings dataframe
        standings_df.insert(len(standings_df.columns),"five_game_average",avg_points_list)
