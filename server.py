"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session 
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/registration")
def new_user():
    """Shows new user registation form."""

    return render_template("registration_form.html")

@app.route("/submit-registration", methods=["POST"])
def submitted():
    """Confirms new user has been registered."""

    email = request.form.get("email")
    password = request.form.get("password")

    if User.query.filter_by(email=email).all():
        flash("Email already registered")
        return redirect("/registration")
    else:
        new_user = User(email=email, 
                        password=password)
        db.session.add(new_user)
        db.session.commit()

        return render_template("submitted.html", email= email)



@app.route("/login-form")
def log_in():
    """Shows form for user to log in."""

    return render_template('login-form.html')



@app.route("/handle-login", methods=["GET", "POST"])
def handle_login():
    """Action for login form: log a user in"""

    
    form_email = request.form.get('email')
    form_password = request.form.get('password')
    user = User.query.filter(User.email == form_email).first()

    if user:
        if form_password == user.password:
            session['user'] = user.user_id

            flash(("Logged in as {}").format(user.email))
            return redirect('/')
        else:
            flash("Wrong password")
            return redirect("/login-form")
    else:
        flash("You have not registered yet. Please do so.")
        return redirect("/registration")

@app.route("/log-out")
def user_log_out():
    """User Logs Out"""

    session.pop('user')

    flash("You successfully logged out")
    return redirect('/')


@app.route("/users/<int:user_id>")
def user_info(user_id):
    """Provide user info"""

    user = User.query.filter_by(user_id=user_id).first()

    age = user.age
    zipcode = user.zipcode
    ratings_from_user = user.ratings

    return render_template("user_info.html", user_id=user_id,
                                            age=age,
                                            zipcode=zipcode,
                                            ratings_from_user=ratings_from_user)

@app.route("/movies")
def movie_list():
    """Show list of movies."""

    movies = Movie.query.order_by(Movie.title).all()
    return render_template("movie_list.html", movies=movies)


@app.route("/movies/<int:movie_id>")
def movie_info(movie_id):
    """Provide movie info"""

    movie = Movie.query.filter_by(movie_id=movie_id).first()

    ratings_for_movie = movie.ratings
    title = movie.title
    release_date = movie.released_at
    movie_url = movie.imdb_url
    movie_id = movie.movie_id

    return render_template("movie_info.html", ratings_for_movie=ratings_for_movie,
                                                title = title,
                                                release_date = release_date,
                                                movie_url = movie_url,
                                                movie_id=movie_id)


@app.route("/handle-rating", methods=["POST"])
def submitted_rating():
    """Updates ratings table."""

    submit = request.form.get("movie_rating")
    movie_id = request.form.get("movie_id")

    logged_in_user_id = session['user']

    if logged_in_user_id:

        booger
        #handle rating
        if Rating.query.filter_by(user_id =logged_in_user_id, movie_id=movie_id):
            print "UPdate "

            # if movie_rating is in 
             # if raing is there update
        else:
            print "commit"
             # add rating and commit  
        # flash("Email already registered")
        # return redirect("/registration")
    else:
    #     #send to homepage, flash "log in to rate this movie"
    #     new_movie_rating = Rating(email=email, 
    #                     score=score)
    #     db.session.add(new_user)
    #     db.session.commit()
        print "got to else condition"
        return render_template("homepage.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
