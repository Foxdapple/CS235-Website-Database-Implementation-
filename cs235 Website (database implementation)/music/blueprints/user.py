from flask import Blueprint, redirect, render_template, url_for, make_response, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from music.domainmodel.user import User
from music.domainmodel.review import Review
import music.adapters.repository as repo
import random

user_blueprint = Blueprint('user_bp', __name__)
database = repo.repo_instance

def create_some_track():
    num_items = database.get_num_tracks()
    index = random.randint(0, num_items)
    some_track = database.get_track_by_id(index)
    while some_track is None:
        index = random.randint(0, num_items)
        some_track = database.get_track_by_id(index)
    return some_track


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    some_track = create_some_track()
    number_of_entries = database.get_number_of_users()
    form = UserForm()
    message = ""
    if form.validate_on_submit():
        user_id = number_of_entries+1
        username = form.username.data
        password = form.password.data
        user_in_db = database.get_user(username.lower())
        if user_in_db is None:
            new_user = User(user_id, username, password)
            database.add_user(new_user)
            message = "User registered, navigate to login to login."
            return render_template('track_list.html', track=some_track, message=message)
        else:
            message = "Username already exists, please choose another."
    return render_template('user_access.html', form=form, handler_url="register", track=some_track, message=message, title="Register")


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    some_track = create_some_track()
    resp = make_response(redirect(url_for("body_bp.body")))
    form = UserForm()
    message = ""
    if form.validate_on_submit():
        username = form.username.data.lower()
        login_password = form.password.data
        user = database.get_user(username)
        message = "User doesn't exist"
        if user is not None:
            if login_password == user.password:
                resp.set_cookie('User', user.user_name)
                return resp
    return render_template('user_access.html', form=form, handler_url="login", track=some_track, message=message, title="Login")


@user_blueprint.route('/logout')
def logout():
    resp = make_response(redirect(url_for("body_bp.body")))
    user = request.cookies.get('User')
    if user is not None:
        resp.set_cookie('User', user, expires=0)
    return resp


@user_blueprint.route('/user_review', methods=['GET', 'POST'])
def write_review():
    tracks = database.get_track_list()
    username = request.cookies.get('User')
    if username is None:
        return redirect(url_for("track_bp.list_track"))
    some_track = create_some_track()
    form = ReviewForm()
    if form.validate_on_submit():
        review = form.review.data
        track_info = request.form.get('track_name')
        track_id = track_info.split(" ")[-1].split(">")[0]
        track = database.get_track_by_id(int(track_id))
        rating = int(request.form.get('rating'))
        if review is not None and track is not None and rating is not None:
            new_review = Review(track, review, rating)
            user = database.get_user(username)
            database.add_review(new_review)
            database.add_user_to_review(review, user)
            return render_template('track_list.html', track=some_track, message="Review successfully added")

    return render_template('review_write.html', form=form, handler_url="user_review", track=some_track, track_list=tracks)


class UserForm(FlaskForm):
    username = StringField("username", [DataRequired(message="Please enter a Username")])
    password = StringField("password", [Length(min=7)])
    submit = SubmitField("Submit")


class ReviewForm(FlaskForm):
    review = StringField("Review:", [DataRequired(message="Please enter a Review")])
    submit = SubmitField("Submit")