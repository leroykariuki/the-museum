from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///Museums.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Join table for museum-artists many to many relationship
museum_artist = Table(
    'museum_artists',
    Base.metadata,
    Column('museum_id', ForeignKey('museums.id'), primary_key = True),
    Column('artists_id', ForeignKey('artists.id'), primary_key = True)
)


class Museums(Base):
    _tablename_ = 'museums'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), index=True)
    location = Column(String())
    year_built = Column(Integer())

    #One to many relationship with Artworks
    artworks = relationship('Artworks', backref=backref('museum'))

    # create one to many relationship with Artists
    artists = relationship('Artists', secondary=museum_artist, back_populates='museums')