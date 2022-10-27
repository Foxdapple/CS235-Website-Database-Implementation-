"""Initialize Flask app."""

# from pathlib import Path

from flask import Flask
from music.adapters.csvdatareader import TrackCSVReader
from music.adapters import database_repository
from music.adapters.abstract_repository import new_repository as new_repo
from music.adapters.orm import metadata, map_model_to_tables
from music.adapters.csv_data_importer import create_objects

import music.adapters.repository as repo
from flask_wtf.csrf import CSRFProtect

# imports from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

def create_app():
    app = Flask(__name__)

    app.secret_key = 'very secret'
    CSRFProtect(app)

    data_path = 'music/adapters/data'

    data = TrackCSVReader(data_path+'/raw_albums_excerpt.csv', data_path+'/raw_tracks_excerpt.csv')
    tracks = data.read_tracks_file()
    albums = data.read_albums_file()

    testing = False

    database_uri = 'sqlite:///music.db'
    SQLALCHEMY_ECHO = False
    repository_mode = "database"
    if repository_mode == "database":
        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relative to the application in music.db,
        # leading to a URI of "sqlite:///music.db".
        # Note that create_engine does not establish any actual DB connection directly!
        database_echo = SQLALCHEMY_ECHO
        # Please do not change the settings for connect_args and poolclass!
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        if testing or len(database_engine.table_names()) == 0:
            print("Populating database...")
            clear_mappers()
            metadata.create_all(database_engine)
            map_model_to_tables()
            for table in reversed(metadata.sorted_tables):
                database_engine.execute(table.delete())

            create_objects(tracks, albums, repo.repo_instance)  # populates the database.
            print("Population done.")
        else:
            map_model_to_tables()
    else:
        new_repo.populate_tracks(tracks)

    with app.app_context():
        # Register blueprints.
        from .blueprints import body
        app.register_blueprint(body.body_blueprint)

        from .blueprints import track
        app.register_blueprint(track.track_blueprint)

        from .blueprints import user
        app.register_blueprint(user.user_blueprint)

        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.close_session()

    return app
