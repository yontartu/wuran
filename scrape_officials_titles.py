import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
from datetime import datetime

# read in activity data
with open('C:scrapy\\chvitae\\activity_20190214.json') as json_file:
	activity_data = json.load(json_file)

all_activities = activity_data
### TEST DATA ###
# all_activities = activity_data[170:175]
# all_activities = activity_data[172:176]

# all_activities = []
# for a in activity_data:
# 	if a['date'] == "June 05, 2012": # putin test case
# 		all_activities.append(a)
# all_activities = all_activities[7:11]


# loop thru each activity record
for ix, activity in enumerate(all_activities): 
	officials = [] # to be added to 'activity' after populated (or not)
	
	for i, link in enumerate(activity['attendees_links']): # loop through attendees links
		match_link = re.search(r'type=ncv', link)
	
		if match_link: # if link to foreign official 
			name_to_match = activity['attendees'][i].strip() 
			date_to_match = datetime.strptime(activity['date'], '%B %d, %Y').date()
			r = requests.get('http://chinavitae.com/vip/' + link) # navigate to  link
			soup = BeautifulSoup(r.text, 'html.parser')
			results = soup.find_all('span', attrs={'class':'link12'})
			
			appearances_list = [] # construct list of dicts of the official's appearances 
			for i, item in enumerate(results):
				if i % 2 == 0:
					date = item.text
				else:
					new_record = {}
					new_record['date'] = date
					new_record['meeting_text'] = item.text
					appearances_list.append(new_record)

			for i, appearance in enumerate(appearances_list): # loop through appearances
				match_bulletpt = re.search(r'•(.+)\(', appearance['meeting_text'])
				
				if match_bulletpt: # if appearance contains a bullet point
					all_people = re.findall(r'•(.+\))', appearance['meeting_text'])[0].split('•') # extract all people from the appearance
					
					for person in all_people: # loop through all people in appearance
						official_name = re.search(r'[^\(]+', person).group(0).strip()
						official_title = re.search(r'\((.*?)\)$', person).group(1).strip()
						date = datetime.strptime(appearance['date'], '%m/%d/%y').date()

						if date == date_to_match and official_name == name_to_match: # if date of appearance and official name both match
							new_official = {}
							new_official['name'] = official_name
							new_official['title'] = official_title
							
							if new_official not in officials: # check if list doesn't already contain the official
								officials.append(new_official)
	
	activity['foreign_officials'] = officials
	activity['activity_id'] = ix
	print(ix)
	print(activity)


# write new data file
with open('C:data\\activity_20190214_titles.json', 'w') as outfile:
    json.dump(all_activities, outfile, indent=4)