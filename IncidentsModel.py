# Creates an Incidents Model object with an 'incidents' database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Incident(Base):
    __tablename__ = 'incident'
    id = Column(Integer, primary_key = True)
    latitude = Column(String)
    longitude = Column(String)
    description = Column(String)
    start_time = Column(String)
    rating = Column(Integer)
    incident_type = Column(String)
    tags = Column(String)
    reactions = Column(String)

    # Decorator to serialize information from 'Incident' database
    @property
    def serialize(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'description': self.description,
            'start_time': self.start_time,
            'rating': self.rating,
            'incident_type': self.incident_type,
            'tags': self.tags,
            'reactions': self.reactions
            }

engine = create_engine('sqlite:///RaheemIncidents.db')
Base.metadata.create_all(engine)
            
