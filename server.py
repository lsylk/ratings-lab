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
        print "Email already registered"
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



@app.route("/handle-login", methods=["POST"])
def handle_login():
    """Action for login form: log a user in"""

    form_email = request.form['email']
    form_password = request.form['password']

    user = User.query.filter(User.email == form_email).one()

    if form_password == user.password:
        session[user.user_id] = user.email
        # flash("Logged in as {}").format(user.email)
        return redirect('/')
    else:
        # flash("Wrong password")
        return redirect("/login-form")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
