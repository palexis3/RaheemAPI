# Script gets Incident models from 'incident.db' and runs a POST request to staging.raheem.ai

import jsonurl
import requests
from random import randint
import urllib
import json
import sys
import codecs
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from IncidentsModel import Base, Incident


sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stdout)

engine = create_engine('sqlite:///RaheemIncidents.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

address = "http://staging.raheem.ai/"
READ_KEY = "0f40f161fbc3221225dbe7c4296afd53"
WRITE_KEY = "87efbee4277a4cb7fd747b8ebf6729ff"

print "Running Incident Dummy Data for Raheem.ai"
try:
    url = address + "api/v1/incidents?write_key=%s" % WRITE_KEY

    # Getting the rows count
    rows = session.query(Incident).count()
    print "Row count: %s \n" % rows
    
    for incident in session.query(Incident):
        latitude = incident.latitude
        longitude = incident.longitude
        description = incident.description
        start_time = incident.start_time
        rating = incident.rating
        incident_type = incident.incident_type
        tags = incident.tags
        reactions = incident.reactions
        
        # Getting user
        user_url = address + "/api/v1/users/4?write_key=%s" % WRITE_KEY
        user_req = requests.get(user_url)
        if user_req.status_code != requests.codes.ok:
            raise Exception('Could not request this user because of the status code: %s' % user_req.status_code)                         
        user = user_req.json()
        user = jsonurl.query_string(user)
        
        # Currently 5 users in Admin page as of when this script was wrote
        user_id = randint(1, 5)
        
        # Setting Incidents as a dictionary
        data = dict(user_id = user_id, latitude = latitude, longitude = longitude, description = description, rating = rating, incident_type = incident_type, start_time = start_time, user = user, tags_list = tags, reactions_list = reactions)
                            
        # Encoding dictionary
        params = urllib.urlencode(data)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        
        req = requests.post(url, params=params, headers=headers)
        if req.status_code != requests.codes.ok:
            raise Exception('Received an unsuccessful code of %s' % req.status_code)
        
except Exception as err:
    print "Could not post 'incident' data to 'staging.raheem.ai'"
    print err.args
    sys.exit()
    
else:
    print "Successfully Posted Incident model to Raheem.ai"
        
