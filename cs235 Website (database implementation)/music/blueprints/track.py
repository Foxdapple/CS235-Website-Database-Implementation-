from flask import Blueprint, redirect, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


import music.adapters.repository as repo

import random, math

track_blueprint = Blueprint('track_bp', __name__)
database = repo.repo_instance


def create_some_track():
    num_items = database.get_num_tracks()
    index = random.randint(0, num_items)
    some_track = database.get_track_by_id(index)
    while some_track is None:
        index = random.randint(0, num_items)
        some_track = database.get_track_by_id(index)
    return some_track


@track_blueprint.route('/track')
def list_track():
    some_track = create_some_track()
    track_message = ''
    logged_in = False
    if request.cookies.get('User') is not None:
        logged_in = True
    return render_template('track_list.html', track=some_track, message=track_message, logged_in=logged_in)


@track_blueprint.route('/tracks/<int:index>', methods=['POST', 'GET'])
def success(index):
    form = PageView()
    list_of_tracks = database.get_track_list()
    track_length = database.get_num_tracks()
    some_track = create_some_track()
    new_track_list = []
    index = index*10
    previous_index = index-10
    for i in range(previous_index, index):
        if i < track_length:
            new_track_list.append(list_of_tracks[i])
        else:
            break
    if request.form.get('back') is not None:
        if index != 1:
            index = int((index / 10)-1)
            return redirect(url_for('track_bp.success', index=index))
    elif request.form.get('forward') is not None:
        if index != 1:
            index = int((index / 10)+1)
            return redirect(url_for('track_bp.success', index=index))
    return render_template('track_list_all.html', form=form, handler_url=int(index/10), track=some_track, track_list=new_track_list)


@track_blueprint.route('/block_choice', methods=['POST', 'GET'])
def list_some_tracks():
    track_length = database.get_num_tracks()
    page_num = int(math.ceil(track_length/10))
    some_track = create_some_track()
    form = ListSome()
    if request.method == 'POST':
        return redirect(url_for('track_bp.success', index=int(request.form.get('index'))))
    else:
        return render_template('track_list_some.html', form=form, handler_url="block_choice", track=some_track, amount=page_num)


@track_blueprint.route('/track_find/<int:track_id>', methods=['POST', 'GET'])
def track_viewer_id(track_id):
    some_track = create_some_track()
    tracks = database.get_track_list()
    track_message = ''
    for track in tracks:
        if track_id == track.track_id:
            review_list = database.get_review_by_track(track_id)
            user_list = database.get_user_by_track(track_id)
            return render_template("track_view.html", artist=track.artist.full_name, song=track.title, album=track.album.title, url=track.track_url, duration=track.track_duration, reviews=review_list, users=user_list, track=some_track)
        else:
            track_message = "Track with specified ID doesn't exist"

    return render_template('track_list.html', track=tracks, message=track_message)


@track_blueprint.route('/track_find_artist/<artist_name>', methods=['POST', 'GET'])
def track_viewer_artist(artist_name):
    new_track_list = []
    form = PageView()
    tracks = database.get_track_list()
    some_track = create_some_track()
    for track in tracks:
        if artist_name == track.artist.full_name:
            new_track_list.append(track)
    return render_template('track_list_all.html', form=form, handler_url=artist_name, track=some_track, track_list=new_track_list)


@track_blueprint.route('/track_find_track/<track_title>', methods=['POST', 'GET'])
def track_viewer_title(track_title):
    new_track_list = []
    tracks = database.get_track_list()
    form = PageView()
    some_track = create_some_track()
    for track in tracks:
        if track.title is not None:
            if track_title == track.title:
                new_track_list.append(track)
    return render_template('track_list_all.html', form=form, handler_url=track_title, track=some_track, track_list=new_track_list)


@track_blueprint.route('/track_find_genre/<genre_name>', methods=['POST', 'GET'])
def track_viewer_genre(genre_name):
    new_track_list = []
    tracks = database.get_track_list()
    form = PageView()
    some_track = create_some_track()
    genre_found = False
    for track in tracks:
        genres_list = track.genres
        for genre in genres_list:
            if genre.name == genre_name:
                new_track_list.append(track)
                genre_found = True
                break
    if not genre_found:
        logged_in = False
        if request.cookies.get('User') is not None:
            logged_in = True
        return render_template('track_list.html', track=some_track, message="No tracks found with specified genre", logged_in=logged_in)
    return render_template('track_list_all.html', form=form, handler_url=genre_name, track=some_track, track_list=new_track_list)


@track_blueprint.route('/find', methods=['GET', 'POST'])
def find_track():
    some_track = create_some_track()
    tracks = database.get_track_list()
    form = SearchForm()
    if form.validate_on_submit():
        if form.id.data is not None:
            return redirect(url_for("track_bp.track_viewer_id", track_id=int(form.id.data)))
        elif request.form.get('artist') is not None:
            return redirect(url_for("track_bp.track_viewer_artist", artist_name=request.form.get('artist')))
        elif request.form.get('track_name') is not None:
            return redirect(url_for("track_bp.track_viewer_title", track_title=request.form.get('track_name')))
        elif request.form.get('genre_name') is not None:
            return redirect(url_for("track_bp.track_viewer_genre", genre_name=request.form.get('genre_name')))

        else:
            return render_template("track_search.html", form=form, handler_url="find", track=some_track, track_list=tracks)
    else:
        return render_template("track_search.html", form=form, handler_url="find", track=some_track, track_list=tracks)


class SearchForm(FlaskForm):
    # id = IntegerField("<name>", [DataRequired(message="You need to use an ID")])
    id = IntegerField("Search by ID")
    submit = SubmitField("Submit")


class ListSome(FlaskForm):
    submit = SubmitField("Submit")


class PageView(FlaskForm):
    back = SubmitField("<-")
    forward = SubmitField("->")