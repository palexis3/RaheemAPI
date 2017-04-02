# Runs a GET Request against SF Open Data Police Incidents endpoint to then, run a POST Request to local 'IncidentsRoute' script 
# Want ~1000 models

from IncidentsModel import Base, Incident
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import requests
from random import randint
import sys
import json
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stdout)

engine = create_engine('sqlite:///RaheemIncidents.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

print "Creating 1000 incidents to populate 'RaheemIncidents' db"

try:
    # Creating new incidents
    req = requests.get('https://data.sfgov.org/resource/9v2m-8wqu.json')
    if req.status_code != requests.codes.ok:
        raise Exception('Received an unsuccessful status code of %s' % req.status_code)
    
    # Received all json data from SF Incidents Report
    json_data = req.json()
    count = 0
    
    rating = [1,2,3,4,5]
    rating_size = len(rating)
    
    reactions = {1: "Protected", 2: "Relieved", 3: "Safe", 4: "Comforted", 5: "Taken care of", 6: "Heard", 7: "Other Positive", 8: "Threatened", 9: "Disrespected", 10: "Scared", 11: "Intimidated", 12: "Embarrassed", 13: "Angry", 14: "Ignored", 15: "Other Negative"}
    reactions_size = len(reactions)
    
    tags = {1: "Citation", 2: "Arrest", 3: "Police Shooting", 4: "Conversation", 5: "Crime", 6: "Other"}
    tags_size = len(tags)
    
    incident_types = {1: "got pulled over", 2: "called the police", 3: "got stopped on foot", 4: "witnessed police", 5: "other"}
    incident_types_size = len(incident_types)
    
    for count in xrange(1000):
        data = json_data[count]
        
        latitude = data['y']
        longitude = data['x']
        description = data['descript']
        start_time = data['date']
        
        rating = rating[randint(0, rating_size - 1)]
        incident_type = incident_types[randint(1, incident_types_size)]
        tags = tags[randint(1, tags_size)]
        
        # Checks the range of rating to assign a plausible reactions value
        if 3 <= rating <= 5:
            reactions = reactions[randint(1, 7)]
        else:
            reactions = reactions[randint(8, reactions_size)]

        print "Rating: %s" % rating
        print "Incident Type: %s" % incident_type
        print "Tags: %s" % tags
        print "Reactions : %s" % reactions
        sys.exit()

        incident = Incident(latitude = latitude, longitude = longitude, description = description, rating = rating, incident_type = incident_type, start_time = start_time, tags = tags, reactions = reactions)
        session.add(incident)
        session.commit()

except Exception as err:
    print "Failed to populate 'RaheemIncidents' db with 1000 models"
    print err.args
    sys.exit()
    
else:
    print "Successully populated 'RaheemIncidents' db with 1000 incident models"
    
    

