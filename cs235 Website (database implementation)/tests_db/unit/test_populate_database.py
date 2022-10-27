from sqlalchemy import select, inspect

from music.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['users', 'user_review', 'tracks', 'albums', 'artists', 'genres']

def test_database_populate_select_all_genres(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['name'])

        assert all_genre_names == ['pop', 'rock', 'metal', 'jazz']

def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['thorke', 'fmercury']

def test_database_populate_select_all_reviews(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_comments_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table comments
        select_statement = select([metadata.tables[name_of_comments_table]])
        result = connection.execute(select_statement)

        all_comments = []
        for row in result:
            all_comments.append((row['id'], row['review'], row['rating'], row['track_id']))

        assert all_comments == [(1, "review", 3, 1),
                                (2, "review2", 3, 2)]

def test_database_populate_select_all_tracks(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_tracks_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_tracks_table]])
        result = connection.execute(select_statement)

        all_tracks = []
        for row in result:
            all_tracks.append((row['id'], row['title']))

        nr_tracks = len(all_tracks)
        assert nr_tracks == 6

        assert all_tracks[0] == (1, 'Gamer')


def test_database_populate_select_all_albums(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_albums_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_albums_table]])
        result = connection.execute(select_statement)

        all_albums = []
        for row in result:
            all_albums.append((row['id'], row['title']))

        nr_albums = len(all_albums)
        assert nr_albums == 6

        assert nr_albums[0] == (1, 'Skyrim')


def test_database_populate_select_all_artists(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_artists_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_artists_table]])
        result = connection.execute(select_statement)

        all_artists = []
        for row in result:
            all_artists.append((row['id'], row['title']))

        nr_artists = len(all_artists)
        assert nr_artists == 6

        assert nr_artists[0] == (1, 'Sever')


