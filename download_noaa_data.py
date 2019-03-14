from ftplib import FTP
from datetime import datetime
import csv
import os.path
import gzip
import pandas as pd


def download_station_data(station, year):
	ftp = FTP('ftp.ncdc.noaa.gov')
	ftp.login()

	print('Accessing data from station ', station)
	# for year in years_list:
	print("Downloading data from {0}...".format(year))
	ftp.cwd("pub/data/noaa/{0}".format(year))
	file_list = ftp.nlst()
	filename = "{0}-{1}-{2}.gz".format(station[0], station[1], year)
	if filename in file_list:
		if os.path.exists("data/noaa/"):
			file = open("data/noaa/{0}".format(filename), "wb")
			ftp.retrbinary("RETR {0}".format(filename), file.write)
			file.close()
		else:
			os.makedirs("data/noaa/")
			file = open("data/noaa/{0}".format(filename), "wb")
			ftp.retrbinary("RETR {0}".format(filename), file.write)
			file.close()
	ftp.cwd("../../../..")
	ftp.quit()
	print('...Done.')


def get_data_from_row(row):
	dt = datetime(int(row[15:19]),int(row[19:21]),int(row[21:23]), int(row[23:25]), int(row[25:27]))
	wind_speed = int(row[65:69])
	wind_direction = row[60:63]
	wind_speed_quality = row[69]
	wind_direction_quality = row[63]
	wind_obs_type = row[64]
	tempc = row[87:92]
	atmpres = row[99:104]
	return dt, wind_speed, wind_direction, wind_speed_quality, wind_direction_quality, wind_obs_type, tempc, atmpres


def write_csv_from_file(filename):
	dt_list = [] # dates
	ws_list = [] # wind speeds
	wd_list = [] # wind directions
	wsq_list = [] # wind speed quality
	wdq_list = [] # wind direction quality
	wot_list = [] # wind observation type code
	temp_list = [] # temperature
	atmp_list = [] # atmospheric pressure
	
	f = gzip.open("data/noaa/" + filename,"rb")
	file_content = f.read()
	f.close()
	file_content = file_content.decode()
	rows = file_content.split("\n")
	
	for row in rows:
		if len(row) > 0:
			dt, ws, wd, wsq, wdq, wot, temp, atmp = get_data_from_row(row)
			dt_list.append(dt)
			ws_list.append(ws)
			wd_list.append(wd)
			wsq_list.append(wsq)
			wdq_list.append(wdq)
			wot_list.append(wot)
			temp_list.append(temp)
			atmp_list.append(atmp)

	df = pd.DataFrame({'date':dt_list, 'wind_speed':ws_list, 'wind_direction':wd_list, 'wind_speed_quality':wsq_list, 'wind_speed_quality':wdq_list, 'wind_obs_type':wot_list, 'tempc':temp_list, 'atmpres':atmp_list})
	df.to_csv('data/noaa/isd_' + filename[-7:-3] + '.csv', index=False)
	print('...Finished writing csv from {0}'.format(filename))


if __name__ == "__main__":

	BEIJING_USAF_WBAN_CODE = [545110, 99999]
	BEIJING_STATION_NAME = 'BEIJING - CAPITAL INTERNATION'
	years = list(range(2008, 2019))	
	bj = BEIJING_USAF_WBAN_CODE

	for year in years:
		download_station_data(bj, year)
		filename = "{0}-{1}-{2}.gz".format(bj[0], bj[1], year)
		write_csv_from_file(filename)
	
	print('Done processing all data!')


	### TESTING ###
	# years = list(range(2008, 2009))	
	# bj = BEIJING_USAF_WBAN_CODE

	# for year in years:
	# 	download_station_data(bj, year)
	# 	filename = "{0}-{1}-{2}.gz".format(bj[0], bj[1], year)
	# 	# write_csv_from_file(filename)
	# 	f = gzip.open("data/noaa/" + filename,"rb")
	# 	file_content = f.read()
	# 	f.close()
	# 	file_content = file_content.decode()
	# 	rows = file_content.split("\n")
	# 	print(rows[0])		
