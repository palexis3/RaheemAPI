# Script reads a CSV file and creates Raheem API Data to post to Raheem API

import requests
import datetime
import sys
import codecs
import pandas
import argparse
import traceback
import urllib
import jsonurl
from itertools import izip
from random import randint

address = "http://staging.raheem.ai/"
READ_KEY = "0f40f161fbc3221225dbe7c4296afd53"
WRITE_KEY = "87efbee4277a4cb7fd747b8ebf6729ff"
MAX_RECORDS = 1000

try:
    # Argument parser takes filename, which must be a CSV
    parser = argparse.ArgumentParser(description="Reads a CSV file")
    parser.add_argument("-i", dest="filename", required=True, help="Input file must be a CSV file", metavar="FILE")
    parser.add_argument("-count", "--num")
    args = parser.parse_args()

    # Reading CSV File
    data = pandas.read_csv(args.filename)
    num = int(args.num)

    if num > MAX_RECORDS:
        print "Number of incidents requested exceeded the max of %s" % MAX_RECORDS
        sys.exit()
    
    # Parsing latitude and longitude
    latitude_variations = ['latitude', 'lat', 'Latitude', 'LATITUDE']
    longitude_variations = ['longitude', 'long', 'Longitude', 'LONGITUDE']

    latitude = None
    longitude = None

    # Loop thorough latitude and longitude arrays to see if their variations exist in the current CSV file
    for lat in latitude_variations:
        if lat in data.columns:
            latitude = data[lat]
            break

    if latitude is None:
        print "THERE IS NO LATITUDE COLUMN IN THIS CSV!"
        sys.exit()

    for longi in longitude_variations:
        if longi in data.columns:
            longitude = data[longi]
            break

    if longitude is None:
        print "THERE IS NO LONGITUDE COLUMN IN THIS CSV!"
        sys.exit()
        

    if len(longitude) != len(latitude):
        print "Longitude and Latitude datasets don't have the same length"
        sys.exit()

    url = address + "api/v1/incidents?write_key=%s" % WRITE_KEY
    
    reactions = {1: "Protected", 2: "Relieved", 3: "Safe", 4: "Comforted", 5: "Taken care of", 6: "Heard", 7: "Other Positive", 8: "Threatened", 9: "Disrespected", 10: "Scared", 11: "Intimidated", 12: "Embarrassed", 13: "Angry", 14: "Ignored", 15: "Other Negative"}
    reactions_size = len(reactions)

    tags = {1: "Citation", 2: "Arrest", 3: "Police Shooting", 4: "Conversation", 5: "Crime", 6: "Other"}
    tags_size = len(tags)

    incident_types = {1: "got pulled over", 2: "called the police", 3: "got stopped on foot", 4: "witnessed police", 5: "other"}
    incident_types_size = len(incident_types)
    count = 0

    for lat, longi in izip(latitude, longitude):

        # Condition checks the num of records to get
        if count == num:
            break
        
        rate = randint(1,5)
        incident_type = incident_types[randint(1, incident_types_size)]
        tag = tags[randint(1, tags_size)]

        # Checks the range of the rating to assign a plausible reactions value
        if 3 <= rate <= 5:
            reaction = reactions[randint(1, 7)]
        else:
            reaction = reactions[randint(8, reactions_size)]

        rate = str(rate)

        # Get all users currently in Raheem Staging API
        users_url = address + "/api/v1/users?write_key=%s" % WRITE_KEY
        users_req = requests.get(users_url)
        if users_req.status_code != requests.codes.ok:
            raise Exception('Could not request Users from staging API because of the status code: %s' % users_req.status_code)
        users_list = users_req.json()
        
        # Randomly getting a user
        user = users_list['data'][randint(0, len(users_list))]
        user_id = user['id']
        user = jsonurl.query_string(user)

        # Getting current date
        date = datetime.datetime.now().strftime('%s')

        # Constructing an Incident as a dictionary
        data = dict(user_id = user_id, user = user, latitude = lat, longitude = longi, rating = rate, incident_type_name = incident_type, tags_list = tag, reactions_list = reaction, start_time = date)

        # Encoding dictionary
        params = urllib.urlencode(data)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        print "Params: \n %s \n" % params

        continue

        # Sending a POST Request to Raheem
        req = requests.post(url, params=params, headers=headers)
        if req.status_code != requests.codes.ok:
            raise Exception('Could not POST to Raheem because of status code: %s' % req.status_code)
        count = count + 1

except Exception as err:
    print "Failed to generate Raheem API data from CSV"
    print err.args
    traceback.print_exc()
    sys.exit()
    
else:
    print "Successfully converted CSV file to Raheem API Data"
        
        
    

    






