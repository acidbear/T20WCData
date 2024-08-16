import os, json
import pandas as pd
import numpy as np

path_to_json = "icc_womens_t20_world_cup_female_json"
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

## Creating the match overviews csv (ICC_Cup_Data.csv)

# Reading from json, compiling all info into a single dataframe
dfs = []
for index, js in enumerate(json_files):
    data = json.load(open(f"{path_to_json}/{js}"))
    data2 = pd.DataFrame.from_dict(data['info'],orient='index')
    dfs.append(data2.transpose())

matches = pd.concat(dfs,ignore_index=True)

# Runs down all teams (1/2), and creates a list of lists of players to be turned into a column
matches['Team 1'] = matches['teams'].str[0]
matches['Team 2'] = matches['teams'].str[1]

team1Players,team2Players = [],[]
for idx,x in enumerate(matches['Team 1']):
    team1Players.append(matches['players'].iloc[idx][x])

for idx,x in enumerate(matches['Team 2']):
    team2Players.append(matches['players'].iloc[idx][x])

# Expanding out dictionaries into their individual columns
matches = pd.concat([matches, matches['officials'].apply(pd.Series),
                             matches['event'].apply(pd.Series),
                             matches['toss'].apply(pd.Series).rename(columns={'winner' : "toss winner"}),
                             matches['outcome'].apply(pd.Series),
                             pd.Series(team1Players).rename("Team 1 Players"),
                             pd.Series(team2Players).rename("Team 2 Players")
                             ], axis=1)

#'by' is stored under outcome, so needs to be dealt with seperately
matches = pd.concat([matches,matches['by'].apply(pd.Series)],axis=1)


matches.rename(columns={'dates' : 'date','method':'used D/L','result' :'was result?',
                        'decision':'decision from toss','runs': 'won by (runs)',
                        'wickets':'won by (wickets)'},inplace=True)

# Removes values in each of these columns from being wrapped in a list
unlist = ['date','player_of_match','tv_umpires','reserve_umpires','match_referees']
for k in unlist:
    matches[k] = matches[k].str[0]

def loser_calc(row):
    # Returns the loser from each match
    if row['Team 1'] == row['winner']:
        return row['Team 2']
    return row['Team 1']

# Cleaning up / creating some additional columns
matches['Umpire 1'] = matches['umpires'].str[0]
matches['Umpire 2'] =  matches['umpires'].str[1]
matches['date'] = pd.to_datetime(matches['date'],format="%Y-%m-%d")
matches['group'] = "Group "+matches['group']
matches['stage'] = matches['stage'].fillna(matches['group'])
matches['loser'] = matches.apply(loser_calc,axis = 1)
matches['was result?'].replace({'no result' : False},inplace=True)
matches['used D/L'].replace({'D/L' : True},inplace=True)

# Selects and orders desired columns
ordered = matches[['date','season','stage','match_number', 'Team 1','Team 2','city','venue','Team 1 Players','Team 2 Players','toss winner','decision from toss',
                   'Umpire 1','Umpire 2','tv_umpires','reserve_umpires','match_referees','winner','loser','won by (runs)','won by (wickets)',
                   'was result?','used D/L','player_of_match']]

# Sort by date, and order of matches played, then save to a csv
ordered.sort_values(by=['date','match_number'],inplace=True)
ordered.to_csv(path_or_buf="ICC_Cup_Data.csv",index=False)



## Creating the list of players and their respective countries ("WCPlayersList.csv")

NAME_CHANGES = {
    "NR Sciver": "NR Sciver-Brunt",
    "KH Brunt" : "KH Sciver-Brunt",
}

def namecheck(player):
    # Checks if a player has an updated name, and if so, returns that updated name
    try:
        return NAME_CHANGES[player]
    except KeyError:
        return player

def add_players_to_country(row):
    players_dict[row['Team 1']] = players_dict[row['Team 1']] + row['Team 1 Players']
    players_dict[row['Team 2']] = players_dict[row['Team 2']] + row['Team 2 Players'] 
    return row
    
# Assigns each player a country
playersdf = ordered[['Team 1','Team 2', 'Team 1 Players','Team 2 Players']].copy()
all_teams = list(set(np.concatenate([playersdf['Team 1'].unique(),playersdf['Team 2'].unique()],axis=0)))  # all teams who've played in the competitions
players_dict = dict(zip(sorted(all_teams),[[]] * len(all_teams))) # dict with keys:country, items:players from the country
playersdf = playersdf.apply(add_players_to_country,axis = 1)

# Removes all duplicates of players from each of the countries
for key,row in players_dict.items():
    players_dict[key] = list(set(list(map(namecheck,row))))

# Creates dataframe and saves to csv
WCPlayersList = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in players_dict.items()]))
WCPlayersList.to_csv(path_or_buf="WCPlayersList.csv",index=False)


