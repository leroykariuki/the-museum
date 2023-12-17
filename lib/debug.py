import ipdb
from models import Museums, Artists, Artworks
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///Museums.db')
session_maker = sessionmaker(bind=engine)
session = session_maker()

if __name__ == "__main__":
    museum1 = session.query(Museums).first()
    artists1 = session.query(Artists).first()
    artwork1 = session.query(Artworks).first()

    ipdb.set_trace()