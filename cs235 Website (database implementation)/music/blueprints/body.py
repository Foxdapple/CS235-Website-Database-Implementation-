from flask import Blueprint, redirect, render_template, url_for, request

from music.domainmodel.track import Track
import music.adapters.repository as repo
import random

body_blueprint = Blueprint('body_bp', __name__)
track = repo.repo_instance

def create_some_track():
    num_items = track.get_num_tracks()
    index = random.randint(0, num_items)
    some_track = track.get_track_by_id(index)
    while some_track is None:
        index = random.randint(0, num_items)
        some_track = track.get_track_by_id(index)
    return some_track


@body_blueprint.route('/')
def body():
    some_track = create_some_track()
    logged_in = False
    if request.cookies.get('User') is not None:
        logged_in = True
    return render_template('body/body.html', track=some_track, logged_in=logged_in)