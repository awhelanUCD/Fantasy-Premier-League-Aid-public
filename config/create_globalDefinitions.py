# Script for generating global_defintions.py file which holds global variables
# Note: in future this should probably be done via a database migration but for
# now this will do

import requests
import pandas as pd

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
json = r.json()
elements_df = pd.DataFrame(json['events'])

gameweek = 1
gameweek_ongoing = False

for element in elements_df.finished:

    if element==False:
        break

    gameweek+=1

gameweek_ongoing=elements_df.iloc[gameweek-1].is_current

print("gameweek: ", gameweek)
print("ongoing?", gameweek_ongoing)

f = open("global_definitions.py", "w")
f.write("CURRENT_GAMEWEEK="+str(gameweek))
f.write("\nGAMEWEEK_ONGOING="+str(gameweek_ongoing))
f.close()
