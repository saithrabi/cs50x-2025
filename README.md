# TRIO FOODS
#### Video Demo:  <[Video](https://youtu.be/gUCvpsFiDBk)>
#### Description:


## Project's roots
The project is originally based on cs50's week 9 pset Finance.
I just wanted to take cs50 web after this so something related i wanted to do and made this demo website for a snacks brand.
As in finance it lets you buy stocks in this app you can buy snacks, create your account and get details about products.

## Explaining site's functionality
Like finance it has pages for Login, Register, Buy, Home and Logout.
You can buy snacks.

## Set-up the coding environment
To start a new project it is better to create a virtual environment first. In this way you can install older versions of specific packages.
Create a virtual environment so that all your necessary packages for project don't collide with system's original packages.
Create virtual environment in the project folder.
First you need to setup the coding environment using npm install Bootstrap and Sass. That we will use in frontend.
After setting up the environment i started building frontend using a layout template.
With this template you don't need to code navbar or footer section in every single page.

## Home page
As for home page it is static displaying snacks and brand information with company's CEO.
The page is customized using sass and Bootstrap for resposiveness. A simple page.


## Buy Page
Buy page consists of a single big form that take input from user about the snack bundles his personal information and sends that form data in the form of mail to company's mail.
The mail is sent using Flask-Mail as for this service to work you need to make some necessary configurations.
I used the Gmail smtp server where you can use your own google mail account for sending mail.
To make this work go to app passwords and generate a password, once generated copy it and paste in configuration.
Now provide a sender email in your message variable and send it using variable_name.send. This will send a mail to company as your order and they will call you to confirm order.

## Media Usage
To make this site more optimized and fast all the pictures were converted from png format to webq format.

## app.py
Notice how most routes are “decorated” with @login_required (a function defined in helpers.py too). That decorator ensures that, if a user tries to visit any of those routes, he or she will first be redirected to login so as to log in.

## Helpers.py
Next take a look at helpers.py. Ah, there’s the implementation of apology. Notice how it ultimately renders a template, apology.html. It also happens to define within itself another function, escape, that it simply uses to replace special characters in apologies. By defining escape inside of apology, we’ve scoped the former to the latter alone; no other functions will be able (or need) to call it.

Next in the file is login_required. No worries if this one’s a bit cryptic, but if you’ve ever wondered how a function can return another function, here’s an example!

## requirements.txt
Next take a quick look at requirements.txt. That file simply prescribes the packages on which this app will depend.

## static/
All the CSS lives in there.

## scss/
All the scss lives in there.

## templates/
Now look in templates/. In login.html is, essentially, just an HTML form, stylized with Bootstrap. In apology.html, meanwhile, is a template for an apology. Recall that apology in helpers.py took two arguments: message, which was passed to render_template as the value of bottom, and, optionally, code, which was passed to render_template as the value of top. Notice in apology.html how those values are ultimately used!

Last up is layout.html. It’s a bit bigger than usual, but that’s mostly because it comes with a fancy, mobile-friendly “navbar” (navigation bar), also based on Bootstrap. Notice how it defines a block, main, inside of which templates (including apology.html and login.html) shall go. It also includes support for Flask’s message flashing so that you can relay messages from one route to another for the user to see.

## TESTING

- registering a new user and verifying that their portfolio page loads with the correct information,
- requesting a quote using a valid stock symbol,
- purchasing one stock multiple times, verifying that the portfolio displays correct totals,
- selling all or some of a stock, again verifying the portfolio, and
- verifying that your history page shows all transactions for your logged in user.
- inputting alphabetical strings into forms when only numbers are expected,
- inputting zero or negative numbers into forms when only positive numbers are expected,
- inputting floating-point values into forms when only integers are expected,
- trying to spend more cash than a user has,
- trying to sell more shares than a user has,
- inputting an invalid stock symbol, and
- including potentially dangerous characters like ' and ; in SQL queries.

