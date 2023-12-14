#!/usr/bin/env python3
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Museums, Artists, Artworks, museum_artist
import click
import sys

engine = create_engine('sqlite:///Museums.db')
session_maker = sessionmaker(bind=engine)
session = session_maker()

while True:
    text = "Welcome to The Museum!"
    click.echo(text.center(100))
    @click.group()
    def cli():
        "The Museum"