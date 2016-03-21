#!/usr/bin/python

from twitter import *

import sys
import csv

latitude = 17.4453194	# geographical centre of search
longitude = 78.3462162	# geographical centre of search
max_range = 100 		# search range in kilometres
num_results = 5000		# minimum results to obtain
outfile = "output.csv"

config = {}
execfile("config.py", config)

twitter = Twitter(
		        auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

csvfile = file(outfile, "w")
csvwriter = csv.writer(csvfile)

row = [ "User", "Text", "Time", "Latitude", "Longitude" ]
input_data = open('myfile','w')
csvwriter.writerow(row)

# the twitter API only allows us to query up to 100 tweets at a time.
# to search for more, we will break our search up into 10 "pages", each
# of which will include 100 matching tweets.

result_count = 0
last_id = None
prev_date = 0
while result_count <  num_results:

	# perform a search based on latitude and longitude
	query = twitter.search.tweets(q = "", geocode = "%f,%f,%dkm" % (latitude, longitude, max_range), count = 100, max_id = last_id)

	for result in query["statuses"]:
		# only process a result if it has a geolocation
		if result["geo"]:
			user = result["user"]["screen_name"]
			text = result["text"]
			text = text.encode('ascii', 'replace')
			time = result['created_at']
			date = time.split(' ')[2]
			date = int(date)
			if prev_date == (date + 1):
				print prev_date
				print date
				input_data.write('\n\n\n')
				input_data.write('Date Changed\n')
				input_data.write('\n\n\n')
			prev_date = date
			latitude = result["geo"]["coordinates"][0]
			longitude = result["geo"]["coordinates"][1]
			
			input_data.write(text)
			input_data.write('\n')
			# now write this row to our CSV file
			row = [ user, text, time, latitude, longitude ]
			csvwriter.writerow(row)
			result_count += 1
		last_id = result["id"]

	print "got %d results" % result_count

csvfile.close()

print "written to %s" % outfile
