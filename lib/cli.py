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

    @cli.command()
    def open():
        # stack to store history
        history = []
        def append(func):
            history.append(func)

        def back():
            function = history.pop()
            function()

        """Enter The Museum"""
        museum_dict = {}
        
        # Display available museums
        def display_museums():
            invite = "Available Museums: "
            click.echo(invite.center(100))
            list_museums = session.query(Museums).all()
            session.close()
            for i, museum in enumerate(list_museums, 1):
                click.echo(f"{i}. {museum.name}")
                museum_dict[i] = museum.name
            append(display_museums)
        display_museums()
    

        museum_choice = click.prompt("\nSelect Museum", type=int)
