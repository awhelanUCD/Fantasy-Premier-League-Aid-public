import requests
import json
import pandas as pd

def getLivePlayerStats(gameweek):

        """
        Function to get live gameweek stats for football players during the gameweek

        :param gameweek: the gameweek that is ongoing
        :type gameweek: int

        :return: live player data object
        :rtype: pandas dataframe
        """

        url = 'https://fantasy.premierleague.com/api/event/'+str(gameweek) +'/live/'
        r_live = requests.get(url)
        json_live = r_live.json()
        elements_live_stats_df = pd.DataFrame(json_live['elements'])

        return elements_live_stats_df

def getPointsByElementAndCreateTeamInfo(picks_df,elements_live_stats_df,transferCost,slim_elements_df):

    """
    Function which returns the total points that a fpl player has gotten so far
    this gameweek as well as a pandas dataframe giving information on the team that they have picked

    :param picks_df: the players that a fpl player has picked
    :type picks_df: pandas dataframe

    :param elements_live_stats_df: contains the live stats for all football players
    :type elements_live_stats_df: pandas dataframe

    :param transferCost: the points lost by a fpl player due to transfers
    :type transferCost: int

    :param slim_elements_df: contains team info of a fpl player
    :type slim_elements_df: pandas dataframe

    :return: total points of an fpl player
    :rtype: int

    :return: final_df: team info of a given fpl player
    :rtype: pandas dataframe
    """

    # Initialise total points
    total_points=0

    # Take relevant columns from picks_df
    picks_df_slim=picks_df[['element','position','multiplier']]

    # Create empty list where the points each football player has acccrued is held
    points_list=[]

    # Iterate through each football player picked
    for i,element in enumerate(picks_df['element']):
       points=elements_live_stats_df['stats'][element-1]['total_points']
       points_list.append(points)

       # See what the multiplier to apply for each football player picked
       # e.g. 0 for a sub, 2 for a captain
       multiplier=picks_df.iloc[i]['multiplier']
       total_points+=points*multiplier

    # Add points column to picks_df_slim dataframe
    picks_df_slim.insert(len(picks_df_slim.columns),"points",points_list)

    # Initialise lists for columns that will be merged with picks_df_slim
    # for final_df
    web_name_list=[]
    team_list=[]
    element_type=[]

    # Columns for dataframe
    columns = ['id','web_name', 'team','element_type']

    # Initialise dataframe
    check_df = pd.DataFrame(columns=columns)
    for i,element in enumerate(picks_df['element']):

        # Add relevant row containing football player information to check_df
        row=slim_elements_df.loc[slim_elements_df['id'] == element]
        check_df = pd.concat([check_df, row], ignore_index=True)

    # Merge dataframe to create final_df
    final_df = pd.merge(picks_df_slim, check_df, left_index=True, right_index=True, how='left')

    return total_points-transferCost,final_df

def createPicksDf(entry, gameweek):

    """
    Returns the cost accrued by a fpl player due to transfers as well as a
    dataframe giving the football players they have picked

    :param entry: the id of a given fpl player
    :type entry: int

    :param gameweek: the gameweek that is ongoing
    :type gameweek: int

    :return: points deducted due to transfers
    :rtype: int

    :return: picks_df: the football players a fpl player has picked for a given
    gameweek
    :rtype: pandas dataframe
    """

    url='https://fantasy.premierleague.com/api/entry/'+str(entry)+'/event/'+str(gameweek) +'/picks/'
    r_team = requests.get(url)
    json_team = r_team.json()
    picks_df=pd.DataFrame(json_team['picks'])
    transferCost=json_team['entry_history']['event_transfers_cost']
    return transferCost,picks_df

def getTotalPlayers():

    """
    Returns the total number of registered people playing fantasy premier league

    :return: total number of fpl players
    :rtype: int
    """

    # Import data from fpl api
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    r = requests.get(url)
    json = r.json()

    # Return total players
    return json['total_players']
