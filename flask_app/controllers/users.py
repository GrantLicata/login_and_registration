from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    print("This is the session:", session)
    return render_template("logreg.html")


@app.route('/register', methods=["POST"])
def register():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    passwords = {
        "password": request.form["password"],
        "confirm_password": request.form["confirm_password"]
    }
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email": request.form["email"],
        "password" : pw_hash,
        "birthday" : request.form["birthday"],
        "gender" : request.form["gender"],
        "language" : request.form["language"]
    }
    print(data['email'])
    session['user_id'] = User.get_by_email(data)
    # Post validation (will cause redirect if False)
    if not User.validate_user(data):
        return redirect('/')
    if not User.validate_password(passwords):
        return redirect('/')
    User.save(data)
    return redirect('/profile')


@app.route('/login', methods=['POST'])
def login():
    data = { 
        "email" : request.form["email"] 
        }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/profile")

@app.route('/clear')
def clear():
    session.clear()
    print(session)
    return render_template("logreg.html")


@app.route('/profile')
def profile():
    if session == {}:
        return redirect('/')
    return render_template("profile.html")

