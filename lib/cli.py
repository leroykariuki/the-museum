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

        def menu_1():
            click.echo("\nWould you like to:")
            for i, option in enumerate(["Navigate through Museum", "Submit Art for Approval"], 1):
                click.echo(f"{i}. {option}")
            append(menu_1)
        menu_1()    

        choice = click.prompt("\nSelect choice", type=int)
        artwork_dict = {}
        list_artworks = session.query(Artworks).filter(Artworks.museum_id == museum_choice).all()

        if choice == 1:
            def display_art():
                text = f"ON DISPLAY in {museum_dict[museum_choice]}"
                click.echo(text.center(100))
                session.close()
                for i, artwork in enumerate(list_artworks, 1):
                    click.echo(f"{i}. {artwork.name}")
                    artwork_dict[i] = artwork.name
                append(display_art)
            display_art()

            artwork_choice = click.prompt("\nSelect Artwork", type=int)
            selected = session.query(Artworks).filter_by(name=artwork_dict[artwork_choice]).first()
            
            click.echo(
                f"""
                Name: {artwork_dict[artwork_choice]}.
                Artist: {(selected.artist).first_name} {(selected.artist).last_name}.
                Artist Rating: {(selected.artist).rating}
                Date of Artwork:  {selected.date_of_artwork}.
                Date of Exhibition:  {selected.date_of_exhibition}.
                """
                )
        
        elif choice == 2:
            def menu_2():
                click.echo("\nAre you: ")
                for i, selection in enumerate(["New Artist", "Existing Artist"], 1):
                    click.echo(f"{i}. {selection}")
                append(menu_2)
            menu_2()
            
            selected = click.prompt("\nSelect: ")
            def new_artwork():
                art_name = click.prompt("\nEnter Artwork Name: ")
                date_of_artwork = click.prompt("\nEnter Date of Artwork: ")
                date_of_exhibition = click.prompt("\nEnter Exhibition Date: ")

                new_artwork = Artworks(
                    name = art_name,
                    date_of_artwork = date_of_artwork,
                    date_of_exhibition = date_of_exhibition,
                    museum_id = museum_choice,
                    artist_id = existing_artist.id
                )
                session.add(new_artwork)
                session.commit()


            existing_artist = session.query(Artists).order_by(Artists.id.desc()).first()
            if selected == "1":
                def new_artists():
                    rating = click.prompt("\nEnter your rating: ", type=int)
                    if rating < 3:
                        click.echo("CANNOT BE APPROVED! RATING MUST BE HIGHER THAN 3!")
                        display_museums()

                    elif 3 <= rating <= 5:
                        first_name = click.prompt("\nEnter your first name: ")
                        last_name = click.prompt("\nEnter your last name: ")
                        
                        new_artist = Artists(
                            first_name = first_name,
                            last_name = last_name,
                            rating = rating
                        )
                        session.add(new_artist)
                        session.commit()

                        new_artwork()
                        
                        new_data = session.query(Artworks).order_by(Artworks.id.desc()).first()
                        data = museum_artist.insert().values(museum_id = new_data.museum_id, artists_id = new_data.artist_id)
                        session.execute(data)
                        session.commit()
                        click.echo("APPROVED!")
                    append(new_artists)
                new_artists()
            
            elif selected == "2":
                def update_artist():
                    first_name = click.prompt("\nEnter your first name: ")
                    last_name = click.prompt("\nEnter your last name: ")

                    existing_artist = session.query(Artists).filter_by(first_name = first_name, last_name = last_name).first()
                    if existing_artist == None:
                        click.echo("USER NOT FOUND")
                    else:
                        new_artwork()
                        click.echo("APPROVED!")
                    append(update_artist)
                update_artist()

            else:
                click.echo("INVALID INPUT")

        final = click.prompt("\nType (q) to exit")
        if final == "q":
            click.echo("Exiting the Program!") 
            sys.exit()
        
        else:
            click.echo("INVALID INPUT")


                    


    if __name__ == '__main__':
        cli()