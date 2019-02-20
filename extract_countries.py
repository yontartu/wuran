import pandas as pd
import re
import json
from datetime import datetime

# read in country-nationality crosswalk
countries_raw_data = pd.read_csv('C:data\\countries_clean.csv')
xw = pd.DataFrame(countries_raw_data[['nationality','country']]).to_dict()
nationalities = xw['nationality'].values()
countries = xw['country'].values()

# read in activity data
with open('C:data\\activity_20190214_titles.json') as json_file:
	activity_data = json.load(json_file)

all_activities = activity_data
### TEST DATA ###
# all_activities = activity_data[170:175] 
# all_activities = activity_data[172:175]
# all_activities = []
# for a in activity_data:
# 	# if a['date'] == "January 12, 2015": 
# 	if a['date'] == 'July 30, 2003': # testing guinea
# 	# if a['date'] == 'September 26, 2005': # testing dr congo
# 	# if a['date'] == 'April 22, 2012': # testing dprk 
# 		all_activities.append(a)
# all_activities = all_activities[:3]


# loop thru each activity record
for ix, activity in enumerate(all_activities):
	matched_countries = []
	matched_on = []
	blocked_countries = []

	# loop thru foreign_officials
	for i, official in enumerate(activity['foreign_officials']):

		# check if country name matches
		for country in countries:
			matched_on_country = re.search(r'\b{}\b'.format(country), official['title'].lower(), re.I)

			if matched_on_country:
				if country == 'south sudan':
					blocked_countries.append('sudan')
					if country not in matched_countries:
						matched_countries.append(matched_on_country.group(0))
						matched_on.append('country')

				elif country == 'equatorial guinea':
					blocked_countries.append('guinea')
					blocked_countries.append('guinea-bissau')
					blocked_countries.append('papua new guinea')
					if country not in matched_countries:
						matched_countries.append(matched_on_country.group(0))
						matched_on.append('country')

				elif country == 'guinea-bissau':
					blocked_countries.append('guinea')
					blocked_countries.append('equatorial guinea')
					blocked_countries.append('papua new guinea')
					if country not in matched_countries:
						matched_countries.append(matched_on_country.group(0))
						matched_on.append('country')

				elif country == 'papua new guinea':
					blocked_countries.append('guinea')
					blocked_countries.append('guinea-bissau')
					blocked_countries.append('equatorial guinea')
					if country not in matched_countries:
						matched_countries.append(matched_on_country.group(0))
						matched_on.append('country')

				elif country == "democratic people's republic of korea":
					blocked_countries.append('republic of korea')
					if country not in matched_countries:
						matched_countries.append(matched_on_country.group(0))
						matched_on.append('country')

				elif country == 'democratic republic of the congo':
					blocked_countries.append('republic of the congo')
					if country not in matched_countries:
						matched_countries.append(matched_on_country.group(0))
						matched_on.append('country')

				elif country == 'democratic republic of congo':
					blocked_countries.append('republic of congo')
					blocked_countries.append('republic of the congo')
					if country not in matched_countries:
						matched_countries.append(matched_on_country.group(0))
						matched_on.append('country')
						print('blocked countries: ', blocked_countries)

				else: 
					if country not in matched_countries and country not in blocked_countries:
						matched_countries.append(matched_on_country.group(0))
						matched_on.append('country')

		# else check if nationality matches
		for nationality in nationalities:
			if nationality == 'u.s.': # edge case
				matched_on_us = re.search(r'u\.s\.', official['title'].lower(), re.I)
				if matched_on_us:
					idx = list(xw['nationality'].keys())[list(nationalities).index(matched_on_us.group(0))]
					co = list(countries)[idx]
					if co not in matched_countries and co not in blocked_countries:
						matched_countries.append(co)
						matched_on.append('nationality')

			else:
				matched_on_nationality = re.search(r'\b{}\b'.format(nationality), official['title'].lower(), re.I)
				if matched_on_nationality:
					idx = list(xw['nationality'].keys())[list(nationalities).index(matched_on_nationality.group(0))]
					co = list(countries)[idx]
					if co not in matched_countries and co not in blocked_countries:
						matched_countries.append(co)
						matched_on.append('nationality')

	activity['matched_countries'] = matched_countries
	activity['matched_on'] = matched_on
	print(ix)
	print(activity)				

with open('C:data\\activity_titles_countries.json', 'w') as outfile:
    json.dump(all_activities, outfile, indent=4)

