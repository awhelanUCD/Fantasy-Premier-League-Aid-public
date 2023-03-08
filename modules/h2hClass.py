import requests
import pandas as pd
import json

from modules.sharedFunctions.sharedFunctions import *

pd.options.mode.chained_assignment = None

class h2hLeague:


    def __init__(self,leagueNo,currentGameweek,gameweek_ongoing=True):
        self.leagueNo=leagueNo
        self.currentGameweek=currentGameweek
        self.gameweekOngoing=gameweek_ongoing
        self.elementLive_df=getLivePlayerStats(currentGameweek)


    def getCurrentStandings(self):

        """
        Return the current standings of given fpl h2h league

        :return: current standings data object
        :rtype: pandas dataframe
        """

        url = 'https://fantasy.premierleague.com/api/leagues-h2h/' +str(self.leagueNo)+ '/standings/'
        r = requests.get(url)
        json = r.json()
        standings_df = pd.DataFrame(json['standings']['results'])

        return standings_df

    def createForm(self,standings_df):

        """
        Adds a form column to a dataframe which holds the current standings

        :param standings_df: the current standings dataframe
        :type standings_df: pandas dataframe
        """

        # Initialise list which will contain form data for each fpl player
        wld_list=[]

        # Initialise list which will hold datafram containing fixture data for
        # the last 5 gameweeks
        gameweeks_df_list=[]

        # Add dataframe containing fixture data for
        # the last 5 gameweeks to gameweeks_df_list
        for i in range(self.currentGameweek-1,self.currentGameweek-6,-1):
            url = 'https://fantasy.premierleague.com/api/leagues-h2h-matches/league/'+str(self.leagueNo)+'/?event='+str(i)
            r = requests.get(url)
            json = r.json()
            gameweeks_df_list.append(pd.DataFrame(json['results']))

        # Iterate through each entry in the league
        for entry in standings_df['entry']:

            # Initialise string object which describes if a player has won, lost
            # or drawn in a given gameweek
            wld_list_obj=''

            # Iterate through each gameweek dataframe and find if a player
            # has won, lost or drawn
            for gameweeks_df in gameweeks_df_list:

                # note: could probably use .loc to search through this for
                # efficiency instead of iterating through each entry
                for k,entry_1_entry in enumerate(gameweeks_df.entry_1_entry):
                    if entry==entry_1_entry:
                        if gameweeks_df['entry_1_win'][k]==1:
                            wld_list_obj+='W'
                        elif gameweeks_df['entry_1_loss'][k]==1:
                            wld_list_obj+='L'
                        else:
                            wld_list_obj+='D'
                        break

                for k,entry_2_entry in enumerate(gameweeks_df.entry_2_entry):
                    if entry==entry_2_entry:
                        if gameweeks_df['entry_2_win'][k]==1:
                            wld_list_obj+='W'
                        elif gameweeks_df['entry_2_loss'][k]==1:
                            wld_list_obj+='L'
                        else:
                            wld_list_obj+='D'

            # Create wld list for the fpl player
            wld_list.append(wld_list_obj)

        # Add wld form column to standings dataframe
        standings_df.insert(len(standings_df.columns),"form",wld_list)

    def createPercentileColumn(self,df):

        """
        Adds a percentile column to a dataframe which holds the current standings

        :param df: the league standings dataframe
        :type df: pandas dataframe
        """

        totalPlayers=getTotalPlayers()
        percentile_list=[]
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
        df.insert(len(df.columns),"percentile",percentile_list)


class h2hLeague_live(h2hLeague):

    def getFixtures(self):

        """
        This returns a dataframe describing the ongoing fixtures, their scores and initialises
        columns which give each fpl player's current points and whether they are winning, losing
        or drawing

        :return: current fixtures information data object
        :rtype: pandas dataframe
        """

        # Get fixture data from fpl api
        url = 'https://fantasy.premierleague.com/api/leagues-h2h-matches/league/'+str(self.leagueNo)+'/?event='+str(self.currentGameweek)
        r = requests.get(url)
        json = r.json()

        fixtures_df = pd.DataFrame(json['results'])

        # Slim down dataframe to relevant information
        fixtures_slim_id_df=fixtures_df[['entry_1_entry','entry_1_player_name','entry_2_entry','entry_2_player_name']]

        # Initialise lists that give each fpl player's current points and whether they are winning, losing
        # or drawing
        wld=['L']*len(fixtures_slim_id_df.index)
        current_points=[0]*len(fixtures_slim_id_df.index)

        # Add columns to dataframe
        fixtures_slim_id_df.insert(2,"entry_1_wld",wld)
        fixtures_slim_id_df.insert(5,"entry_2_wld",wld)

        fixtures_slim_id_df.insert(3,"entry_1_points",current_points)
        fixtures_slim_id_df.insert(7,"entry_2_points",current_points)

        return fixtures_slim_id_df

    def updateFixtureResults(self, fixtures_df_slimId):

        """
        This fills the win-loss-draw and points columns in the fixtures dataframe
        with up-to-date information.
        In addition, it returns a dataframe containing team information for each
        fantasy premier league player

        :param fixtures_df_slimId: object containg fixture information
        :type df: pandas dataframe

        :return: team information data object
        :rtype: pandas dataframe
        """

        # Get data from fpl api
        url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
        r = requests.get(url)
        json = r.json()
        elements_df = pd.DataFrame(json['elements'])

        # Create dataframe containing relevant information
        slim_elements_df = elements_df[['id','web_name','team','element_type']]

        # Initialise dataframe
        df=pd.DataFrame()

        # Iterate through fixtures
        for i in range(len(fixtures_df_slimId.index)):

            # Find the transfer cost each player has accrued and a dataframe
            # which contains information on the team they have picked
            transferCost,picks_df=createPicksDf(fixtures_df_slimId['entry_1_entry'][i],self.currentGameweek)

            # Return the fpl players current points and and the teamInfo dataframe
            # which incorporates further team information
            current_points1,teamInfo=getPointsByElementAndCreateTeamInfo(picks_df,self.elementLive_df,transferCost,slim_elements_df)

            # The teamInfo dataframe contains football player information for
            # each fpl player
            df=pd.concat([df,teamInfo])

            # Update the points column for the fpl player
            fixtures_df_slimId['entry_1_points'][i]=current_points1

            # Find the transfer cost each player has accrued and a dataframe
            # which contains information on the team they have picked
            transferCost,picks_df=createPicksDf(fixtures_df_slimId['entry_2_entry'][i],self.currentGameweek)

            # Return the fpl players current points and the teamInfo dataframe
            # which incorporates further team information
            current_points2,teamInfo2=getPointsByElementAndCreateTeamInfo(picks_df,self.elementLive_df,transferCost,slim_elements_df)

            # The teamInfo dataframe contains football player information for
            # each fpl player
            df=pd.concat([df,teamInfo2])

            # Update the points column for the fpl player
            fixtures_df_slimId['entry_2_points'][i]=current_points2

            # update wld column
            if current_points1>current_points2:
                fixtures_df_slimId['entry_1_wld'][i]='W'
                fixtures_df_slimId['entry_2_wld'][i]='L'

            elif current_points1<current_points2:
                fixtures_df_slimId['entry_1_wld'][i]='L'
                fixtures_df_slimId['entry_2_wld'][i]='W'
            else:
                fixtures_df_slimId['entry_1_wld'][i]='D'
                fixtures_df_slimId['entry_2_wld'][i]='D'

        return df


    def updateLiveTable(self,updated_standings_df,standings_df,fixtures_df_slimId):

        """
        Method which gives the live standings

        :param updated_standings_df: initial dataframe which will be updated here
        :type updated_standings_df: pandas dataframe

        :param standings_df: contains the standings after the precious gameweek
        :type standings_df: pandas dataframe

        :param fixtures_df_slimId: contains live fixture data
        :type fixtures_df_slimId: pandas dataframe
        """

        # Initialise lists containing wld information and the live results of
        # current fixtures
        wld_list=['-']*len(updated_standings_df.index)
        points_list=['0']*len(updated_standings_df.index)

        # Add lists to dataframe as columns
        updated_standings_df.insert(7,"wld_list",wld_list)
        updated_standings_df.insert(8,"points_list",points_list)

        # Iterate through each entry
        for i,entry in enumerate(updated_standings_df['entry']):

            # Search through fixtures dataframe for corresponding entry
            # note: this should probably be changed to use .loc instead for efficiency
            for k,entry_1_entry in  enumerate(fixtures_df_slimId['entry_1_entry']):

                # Update total points, league points and wld information
                # Only update the wld column when the gameweek has concluded
                # and a new gameweek has not yet started
                if entry==entry_1_entry:
                    if self.gameweekOngoing == True:
                      updated_standings_df['points_for'][i]=standings_df['points_for'][i]+fixtures_df_slimId['entry_1_points'][k]
                    if fixtures_df_slimId['entry_1_wld'][k]=='W':
                        if self.gameweekOngoing == True:
                            updated_standings_df['matches_won'][i]=standings_df['matches_won'][i]+1
                        updated_standings_df['wld_list'][i]='W'
                    elif fixtures_df_slimId['entry_1_wld'][k]=='L':
                        if self.gameweekOngoing == True:
                            updated_standings_df['matches_lost'][i]=standings_df['matches_lost'][i]+1
                        updated_standings_df['wld_list'][i]='L'
                    else:
                        if self.gameweekOngoing == True:
                            updated_standings_df['matches_drawn'][i]=standings_df['matches_drawn'][i]+1
                        updated_standings_df['wld_list'][i]='D'
                    updated_standings_df['points_list'][i]=str(fixtures_df_slimId['entry_1_points'][k])+'-'+str(fixtures_df_slimId['entry_2_points'][k])
                    break

            # Search through fixtures dataframe for corresponding entry
            # note: this should probably be changed to use .loc instead for efficiency
            for k,entry_2_entry in  enumerate(fixtures_df_slimId['entry_2_entry']):

                # Update total points and wld information
                # Only update the wld column when the gameweek has concluded
                # and a new gameweek has not yet started
                if entry==entry_2_entry:
                    if self.gameweekOngoing == True:
                      updated_standings_df['points_for'][i]=standings_df['points_for'][i]+fixtures_df_slimId['entry_1_points'][k]
                    if fixtures_df_slimId['entry_2_wld'][k]=='W':
                        if self.gameweekOngoing == True:
                            updated_standings_df['matches_won'][i]=standings_df['matches_won'][i]+1
                        updated_standings_df['wld_list'][i]='W'
                    elif fixtures_df_slimId['entry_2_wld'][k]=='L':
                        if self.gameweekOngoing == True:
                            updated_standings_df['matches_lost'][i]=standings_df['matches_lost'][i]+1
                        updated_standings_df['wld_list'][i]='L'
                    else:
                        if self.gameweekOngoing == True:
                            updated_standings_df['matches_drawn'][i]=standings_df['matches_drawn'][i]+1
                        updated_standings_df['wld_list'][i]='D'
                    updated_standings_df['points_list'][i]=str(fixtures_df_slimId['entry_1_points'][k])+'-'+str(fixtures_df_slimId['entry_2_points'][k])
                    break

        # Update games played and league points
        if self.gameweekOngoing == True:
          updated_standings_df.matches_played=updated_standings_df.matches_played+1
          updated_standings_df.total=updated_standings_df.matches_won*3+updated_standings_df.matches_drawn*1

    def createChangeList(self,df):

        """
        Adds a column to a dataframe describing if a plyer has risen, fallen or
        stayed in the same position in the table

        :param df: the league standings dataframe
        :type df: pandas dataframe
        """

        change_list=[]
        for i in range(len(df.index)):
            if self.gameweekOngoing == True:
                change=(i+1)-df['Old Rank'][i]
                if change==0:
                    change_list.append('-')
                if change>0:
                    change_list.append('D')
                if change<0:
                    change_list.append('U')

            else:
                change=(i+1)-df['last_rank'][i]
                if change==0:
                    change_list.append('-')
                if change>0:
                    change_list.append('D')
                if change<0:
                    change_list.append('U')

        df.insert(len(df.columns),"change_val",change_list)
