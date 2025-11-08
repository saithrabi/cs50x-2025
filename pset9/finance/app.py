import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Collect info about user with record of shares bought

    id = session["user_id"]
    rows = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM data WHERE user=? GROUP BY symbol HAVING total_shares > 0", id)
    cash = db.execute("SELECT cash FROM users WHERE id=?", id)
    cash = cash[0]["cash"]
    total_cash = cash

    # render new page for new user
    if len(rows) == 0:
        return render_template("index.html", cash=cash, total_cash=total_cash)

    # render page for old user with transactions
    for row in rows:
        symbol = row["symbol"]
        dict = lookup(symbol)
        row["price"] = dict["price"]
        row["value"] = row["price"] * row["total_shares"]
        row["total"] = row["value"]
        total_cash += row["value"]

    return render_template("index.html", rows=rows, cash=cash, total_cash=total_cash)
    # return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    # Verify user data
    if request.method == "POST":

        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("MISSING SYMBOL", 400)

        # Ensure shares is submitted
        if not request.form.get("shares"):
            return apology("MISSING SHARES", 400)
        elif not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("INVALID SHARES", 400)

        # Return the value of symbol
        dict = lookup(symbol)
        if lookup(symbol) == None:
            return apology("INVALID SYMBOL", 400)
        price = dict.get('price')

        # Look for user for cash
        id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id=?", id)
        cash = user_cash[0]["cash"]
        amount_spend = price * float(shares)

        # check if user can afford transaction
        if cash < amount_spend:
            return apology("CAN'T AFFORD", 400)

        updated_cash = cash - amount_spend

        db.execute("UPDATE users SET cash=? WHERE id=?", updated_cash, id)
        db.execute("INSERT INTO record(price, shares, symbol, user_id) VALUES(?, ?, ?, ?)",
                   price, shares, symbol, id)

        # check previous shares and update them
        row = db.execute("SELECT shares FROM data WHERE user=? AND symbol=?", id, symbol)
        if row == []:
            db.execute("INSERT INTO data(shares, symbol, user) VALUES(?, ?, ?)", shares, symbol, id)
        else:
            new_shares = row[0]["shares"]
            new_shares = int(new_shares) + int(shares)
            db.execute("UPDATE data SET shares=? WHERE symbol=? AND user=?", new_shares, symbol, id)

    flash(f"Bought {shares} of {symbol} for {usd(price)}, Updated cash: {usd(updated_cash)}")
    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    id = session["user_id"]
    rows = db.execute("SELECT * FROM record WHERE user_id=?", id)
    if request.method == "GET":
        return render_template("history.html", rows=rows)
    # return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # render quote
    if request.method == "GET":
        return render_template("quote.html")

    # when method is post
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("MISSING SYMBOL", 400)

        # Store symbol
        if request.form.get("symbol"):
            symbol = request.form.get("symbol")

        # Return the value of symbol
        if lookup(symbol) == None:
            return apology("INVALID SYMBOL", 400)
        else:
            dict = lookup(symbol)
            name, price, symboll = dict.get('name'), dict.get('price'), dict.get('symbol')
            return render_template("quoted.html", name=name, price=price, symboll=symboll)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    try:
        if request.method == "POST":
            # Ensure username was submitted
            if not request.form.get("username"):
                return apology("must provide username", 400)

        # Ensure password was submitted
            if not request.form.get("password"):
                return apology("must provide password", 400)

        # Ensure confirm password exists
            if not request.form.get("confirmation"):
                return apology("must confirm password", 400)

        # Confirm password
            if not request.form.get("password") == request.form.get("confirmation"):
                return apology("password must match", 400)

        # Hash user's password
            username = request.form.get("username")
            password = request.form.get("password")
            hash = generate_password_hash(password)
        # Register user
            db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, hash)
            return redirect("/")

    except ValueError:
        return apology("user exists", 400)


@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def change():

    if request.method == "GET":
        return render_template("change.html")

    if request.method == "POST":

        if not request.form.get("old password"):
            return apology("must provide old password", 400)

        if not request.form.get("new password"):
            return apology("must provide old password", 400)

        # Ensure confirm password exists
        if not request.form.get("confirm password"):
            return apology("must confirm password", 400)

        # Confirm password
        if not request.form.get("new password") == request.form.get("confirm password"):
            return apology("password must match", 400)

        id = session["user_id"]

        rows = db.execute(
            "SELECT * FROM users WHERE id = ?", id
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("old password")
        ):
            return apology("invalid old password", 403)

        new_password = request.form.get("new password")
        hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash=? WHERE id=?", hash, id)
        return redirect("/login")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Get symbols
    id = session["user_id"]
    symbols = db.execute("SELECT symbol from data WHERE user=?", id)

    # as get
    if request.method == "GET":
        return render_template("sell.html", symbols=symbols)

    # as post
    if request.method == "POST":

        shares = request.form.get("shares")

        # Ensure symbol and shares are provided
        if not request.form.get("symbol"):
            return apology("MISSING SYMBOL", 400)

        if not request.form.get("shares"):
            return apology("MISSING SHARES", 400)

        elif not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("INVALID SHARES", 400)

        # Defining the sold symbol,shares
        sold_symbol = request.form.get("symbol")
        sold_shares = int(request.form.get("shares"))

        shares = db.execute("SELECT shares FROM data WHERE symbol=? AND user=?", sold_symbol, id)
        shares = [d['shares'] for d in shares]
        shares = shares[0]
        shares = int(shares)

        # Ensure user has enough shares to sell
        if shares < sold_shares:
            return apology("TOO MANY SHARES")

        # If user tries to sell all shares
        elif shares == sold_shares:
            dict = lookup(sold_symbol)
            price = dict.get('price')
            price = float(price) * sold_shares
            cash = db.execute("SELECT cash FROM users WHERE id=?", id)
            cash = [d["cash"] for d in cash]
            cash = cash[0]
            cash = float(cash) + float(price)
            sold_shares = "-" + str(sold_shares)
            db.execute("INSERT INTO record(user_id, shares, symbol, price) VALUES(?, ?, ?, ?)",
                       id, sold_shares, sold_symbol, price)
            db.execute("UPDATE users SET cash=? WHERE id=?", cash, id)
            db.execute("DELETE FROM data WHERE user=? AND symbol=?", id, sold_symbol)

        # IF user sells a limited shares
        else:
            new_shares = shares - sold_shares
            dict = lookup(sold_symbol)
            price = dict.get('price')
            price = float(price) * sold_shares
            cash = db.execute("SELECT cash FROM users WHERE id=?", id)
            cash = [d["cash"] for d in cash]
            cash = cash[0]
            cash = float(cash) + float(price)
            sold_shares = "-" + str(sold_shares)
            db.execute("INSERT INTO record(user_id, shares, symbol, price) VALUES(?, ?, ?, ?)",
                       id, sold_shares, sold_symbol, price)
            db.execute("UPDATE users SET cash=? WHERE id=?", cash, id)
            db.execute("UPDATE data SET shares=? WHERE symbol=? AND user=?",
                       new_shares, sold_symbol, id)

    flash(f"Sold {sold_shares} of {sold_symbol} for {usd(price)}, Updated cash: {usd(cash)}")
    return redirect("/")
