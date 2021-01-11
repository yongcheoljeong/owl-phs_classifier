import os 
import pandas as pd 
from tqdm import tqdm
import csv

'''
> Download OWL simple PHS data from here:
https://overwatchleague.com/statslab
'''
# Set directory
base = 'D:/owl-data/simple phs/' # save simple phs files here
save_path = f'./data/' # result csv files will be saved here

season = ['2018', '2019', '2020']

# Save phs as csv files with selected features
for s in season:
    phs_path = base + f'phs_{s}/' # set simple phs files with seasons
    map_stat_file_name = 'match_map_stats.csv'
    file_list = os.listdir(phs_path)
    
    for file_name in file_list:
        
        phs_name = file_name

        map_stat = pd.read_csv(base + map_stat_file_name)
        phs = pd.read_csv(phs_path + phs_name)

        # Select features of interest
        selected_features = ['match_winner', 'map_winner', 'map_loser', 'map_name', 'winning_team_final_map_score', 'losing_team_final_map_score', 'team_one_name', 'team_two_name']
        selected_map_stat = map_stat[selected_features]

        table = list()

        # Export to csv
        with open(phs_path + phs_name, mode='rt', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter = ',')
            for row in tqdm(csv_reader):
                try:
                    match_id = row['esports_match_id'] # feature name of 2020 data
                except:
                    match_id = row['match_id'] # feature name of 2018, 2019 data
                
                map_name = row['map_name']
                
                data = row

                add_stat = selected_map_stat[map_stat['match_id'] == int(match_id)]
                add_stat = add_stat[add_stat['map_name'] == map_name]
                add_stat.reset_index(drop = True, inplace = True)
                add_stat = add_stat.iloc[0]
                add_stat.to_dict()

                data.update(add_stat)
                
                table.append(data)

        t = pd.DataFrame(table)
        # rename the features to make them consistent with 2020 season's feature name
        t.columns = ['start_time', 'esports_match_id', 'tournament_title', 'map_type', 'map_name', 'player_name', 'team_name', 'stat_name', 'hero_name', 'stat_amount', 'match_winner', 'map_winner', 'map_loser', 'winning_team_final_map_score', 'losing_team_final_map_score', 'team_one_name', 'team_two_name']
        t['season'] = s
        
        os.makedirs(save_path, exist_ok=True)
        t.to_csv(f'{save_path}new_{phs_name}', index = False)