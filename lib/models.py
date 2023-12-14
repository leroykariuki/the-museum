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


class Artists(Base):
    _tablename_ = 'artists'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    rating = Column(Integer())

    #One to many relationship with Artworks
    artworks = relationship('Artworks', backref=backref('artist'))

    # create one to many relationship with Artists
    museums = relationship('Museums', secondary=museum_artist, back_populates='artists')

class Artworks(Base):
    _tablename_ = 'artworks'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), index=True)
    date_of_artwork = Column(Integer())
    date_of_exhibition = Column(Integer())
    museum_id = Column(Integer(), ForeignKey('museums.id'))
    artist_id = Column(Integer(), ForeignKey('artists.id'))