import os, json
import pandas as pd
import numpy as np

## RecNo system : First 2 characters are the year of the tournament, next character is either 'a' (first innings) or 'b' (second innings),
## last one or two charcters indicate this is the xth match to take place in the tournament
## ex : 18b7 -> second innings of the 7th game in the 2018 tournament

path_to_json = "icc_womens_t20_world_cup_female_json"
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

## season_counts keeps track of the number of matches from each year (+1) added to individualMatchs
allBalls , allOvers ,indivdualMatches  = [] , [], []
season_counts = dict(zip(["2013/14","2015/16","2018/19","2019/20","2022/23"],[1,1,1,1,1]))

# Extract the data from each ball, and compile into a single dataframe
# ball -> over -> match -> total
for js in json_files:
    data = json.load(open(f"{path_to_json}/{js}"))

    match_date = data['info']['dates'][0]
    match_season = data['info']['season']

    for innings,for_rec in zip(data['innings'],['a','b']):
        for over in innings['overs']:
            for ball in over['deliveries']:
                oneBallDf = pd.DataFrame.from_dict(ball,orient='index')
                allBalls.append(oneBallDf.transpose())

            oneOverDf = pd.concat(allBalls,ignore_index=True)
            oneOverDf['ball no'] = np.arange(len(over['deliveries'])) + 1
            oneOverDf['over no'] = over['over'] + 1
            oneOverDf['batting team'] = innings['team']
            oneOverDf['for_rec'] = for_rec
            allOvers.append(oneOverDf)
            allBalls = []
    match = pd.concat(allOvers,ignore_index=True)   

    match['date'] = pd.to_datetime(match_date,format="%Y-%m-%d")
    match['season'] = match_season

    match['RecNo'] = (match['date'].dt.year.astype(str).str[2:]) + match['for_rec'] + str(season_counts[match_season])
    season_counts[match_season] += 1    # we have seen another match from a certain year, so increment the corresponding number

    indivdualMatches.append(match)
    allOvers = []

totalDf = pd.concat(indivdualMatches,ignore_index=True)


def get_wicket_repl_info(x,repl = False):
    # Utility to extract the info from the wicket and replacement columns (needs to be removed from list)
    if pd.isnull(x):
        return np.nan
    if repl:
        try:
            return (x['role'][0])
        except KeyError:
            return x['match'][0]
    return (x[0])

def get_fielder_name(x):
    # Utility to extract the info from the list of fielders invovled in a wicket (needs to be removed from list)
    try:
        if len(x) > 1:
            return[j['name'] for j in x] 
        else : 
            return x[0]['name']
    except TypeError:
        return np.nan

# Expanding out the columns which contain dictionaries, so each value has it's own column
totalDf = pd.concat([totalDf,totalDf['runs'].apply(pd.Series).rename(columns={'batter':'runs_off_bat','total':'total_off_ball','extras': 'extras_off_ball'})],axis = 1)
totalDf = pd.concat([totalDf,totalDf['extras'].apply(pd.Series)],axis=1)
totalDf = pd.concat([totalDf,totalDf['wickets'].apply(lambda x : get_wicket_repl_info(x)).apply(pd.Series).rename(columns={'kind' : 'dismissal'})],axis = 1)
totalDf = pd.concat([totalDf,totalDf['replacements'].apply(lambda x : get_wicket_repl_info(x,repl=True)).apply(pd.Series).rename(columns={'in':'fielder_in','out':'fielder_out','role':'player_role'})],axis = 1)
totalDf = pd.concat([totalDf,totalDf['review'].apply(pd.Series).rename(columns={'by':'review_by','umpire':'umpire_at_review','batter':'batter_at_review','decision':'review_decision'})],axis=1)
totalDf['fielder_involved'] = totalDf['fielders'].apply(lambda x: get_fielder_name(x))

# Adds running totals for runs scores and wickets taken
innings =  [x for _,x in totalDf.groupby(totalDf['RecNo'])]
for i in innings:
    i['innings total'] = i['total_off_ball'].cumsum()
    i['wickets_fallen'] = i['player_out'].apply(lambda x: 0 if pd.isnull(x) else 1).cumsum()  
totalDf = pd.concat(innings,ignore_index=True)

# Selects and orders desired columns
totalDfOrdered = totalDf[['date','season','RecNo','batting team','batter','non_striker','bowler','ball no','over no',
                          'runs_off_bat','extras_off_ball','legbyes','wides','byes','noballs','total_off_ball','innings total', 'wickets_fallen',
                          'player_out','dismissal','fielder_involved','fielder_in','fielder_out','reason','player_role',
                          'review_by','umpire_at_review','batter_at_review','review_decision','umpires_call','non_boundary']]

# Sort by date, and order of matches played, then save to a csv
totalDfOrdered.sort_values(by=['date','RecNo'],inplace=True)
totalDfOrdered.to_csv(path_or_buf="Ball_by_Ball_Data.csv",index=False)
