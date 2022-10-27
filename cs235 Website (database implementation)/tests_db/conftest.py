import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from music.adapters import database_repository
from music.adapters.orm import metadata, map_model_to_tables
import music.adapters.repository as repo

from utils import get_project_root

TEST_DATA_PATH_DATABASE_FULL = get_project_root() / "music" / "adapters" / "data"
TEST_DATA_PATH_DATABASE_LIMITED = get_project_root() / "tests" / "data"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///music-test.db'

data = TrackCSVReader(data_path + '/raw_albums_test.csv', data_path + '/raw_tracks_test.csv')
tracks = data.read_tracks_file()
albums = data.read_albums_file()

@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    create_objects(tracks, albums, repo.repo_instance)
    yield engine
    metadata.drop_all(engine)

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    create_objects(tracks, albums, repo.repo_instance)
    yield session_factory
    metadata.drop_all(engine)

@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)
