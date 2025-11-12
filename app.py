from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_mail import Mail, Message
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# configuration of mail 
app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'jasonkali007@gmail.com'
app.config['MAIL_PASSWORD'] = 'wdfl ceoe vsfu gkyx'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///trio.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@app.route("/home")
def home():
    """home page"""
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")
            return redirect("/login")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash('Incorrect username or password Plz register')
            return redirect("/register")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")   

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    try:
        if request.method == "POST":
            # Ensure username was submitted
            if not request.form.get("username"):
                flash("must provide username")
                return redirect("/register")

        # Ensure password was submitted
            if not request.form.get("password"):
                flash("must provide password")
                return redirect("/register")

        # Ensure confirm password exists
            if not request.form.get("confirmation"):
                flash("must confirm password")
                return redirect("/register")

        # Confirm password
            if not request.form.get("password") == request.form.get("confirmation"):
                flash("password must match")
                return redirect("/register")

        # Hash user's password
            username = request.form.get("username")
            password = request.form.get("password")
            hash = generate_password_hash(password)
        # Register user
            db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, hash)
            return redirect("/")

    except ValueError:
        return apology("user exists", 400)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # Buy snacks
        
    if request.method == "GET":
        return render_template("buy.html")
    
    if request.method == "POST":
        salty = request.form.get("bundle salty")
        hot = request.form.get("bundle hot")
        broast = request.form.get("bundle broast")
        name = request.form.get("name")
        address = request.form.get("address")
        number = request.form.get("number")
        
        if not number.isdigit():
            flash("Please add a valid number")
            return redirect("/buy")
        list = [salty, hot, broast]
        for item in list:
            if not item.isdigit():
                flash('Please add value in digits')
                return redirect("/buy")
        
            if int(item) < 0:
                flash('Value must be greater than 0')
                return redirect("/buy")
            else:
                pass
    msg = Message(subject="New Order",
        sender="jasonkali007@gmail.com",
        recipients=['mrabi424@gmail.com']
)
    try:
        msg.html=(f"<h4>Name: {name}</h4><h4>Address: {address}</h4><h4>Number: {number}</h4><p>Salty {salty} budles.<br>Hot & Spicy {hot} bundles.<br>Chicken Broast {broast} bundles.</p>")
        mail.send(msg)
        flash("Order Placed.")
        return redirect("/")
    except:
        flash("Some error occured")
        return redirect("/") 
if __name__ =="__main__":
    app.run()
