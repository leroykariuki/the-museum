from models import Museums, Artists, Artworks, museum_artist
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from faker import Faker
import random

engine = create_engine('sqlite:///Museums.db')
session_maker = sessionmaker(bind=engine)
session = session_maker()

fake = Faker()

if _name_ == "_main_":
    # Clearing the database to avoid duplicate data
    print("CLEARING THE DATABASE***")
    session.query(Museums).delete()
    session.query(Artists).delete()
    session.query(Artworks).delete()
    session.query(museum_artist).delete()
    print("DONE!")
    
    
    print("SEEDING MUSEUMS......")
    museums = ["Museum of Bad Art", "International Spy Museum", "Museum of Medieval Torture Instruments", "Museum of Jurassic Technology", "Icelandic Phallological Museum"]
    for museum_name in museums:
        museum = Museums(
            name=museum_name,
            location=fake.city(),
            year_built=fake.date()
        )
        session.add(museum)
        session.commit()
    print("DONE SEEDING MUSEUMS!")
