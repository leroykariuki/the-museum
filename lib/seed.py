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

       print("SEEDING ARTISTS........")
    artists_list = []
    for i in range(20):
        artist = Artists(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            rating=random.randint(1, 5)
        )
        session.add(artist)
        session.commit()
        artists_list.append(artist)
    print("DONE SEEDING ARTISTS!")
       

    print("SEEDING ARTWORKS........")
    for artists in artists_list:
        for i in range(3):
            art = Artworks(
                name= fake.sentence(nb_words = 5),
                date_of_artwork= fake.date(),
                date_of_exhibition= fake.date(),
                museum_id= random.randint(1,5),
                artist_id= artists.id
            )
            session.add(art)
            session.commit()
    print("DONE SEEDING ARTWORKS!")

    print("SEEDING JOIN TABLE......")
    data_list = []
    for piece in session.query(Artworks).all():
        if piece.artist_id not in data_list:
            data_list.append(piece.artist_id)
            # print(data_list)
            # for entry in data_list
            data = museum_artist.insert().values(museum_id = piece.museum_id, artists_id = piece.artist_id)
            session.execute(data)
            session.commit()
    print("DONE SEEDING JOIN TABLE!")


    session.close()
