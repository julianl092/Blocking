import cs50
import csv
from cs50 import SQL
from flask import Flask, jsonify, redirect, render_template, request
from brutealgorithm import *

# Configure application
app = Flask(__name__)
db = SQL("sqlite:///blocking.db")

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return render_template("index.html")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    #Gets user name, seven inputted blockmates and their corresponding ratings from the form; stores in appropriately named variables.
    username = request.form.get("username")
    name1 = request.form.get("name1")
    rating1 = request.form.get("rating1")
    name2 = request.form.get("name2")
    rating2 = request.form.get("rating2")
    name3 = request.form.get("name3")
    rating3 = request.form.get("rating3")
    name4 = request.form.get("name4")
    rating4 = request.form.get("rating4")
    name5 = request.form.get("name5")
    rating5 = request.form.get("rating6")
    name6 = request.form.get("name6")
    rating6 = request.form.get("rating6")
    name7 = request.form.get("name7")
    rating7 = request.form.get("rating7")

    #Inserts form response and user name into "responses" table of SQL database.
    db.execute("INSERT into responses (id1, rating1, id2, rating2, id3, rating3, id4, rating4, id5, rating5, id6, rating6, id7, rating7, id) VALUES (:id1, :rating1, :id2, :rating2, :id3, :rating3, :id4, :rating4, :id5, :rating5, :id6, :rating6, :id7, :rating7, :id)",
                id1 = name1,
                rating1 = rating1,
                id2 = name2,
                rating2 = rating2,
                id3 = name3,
                rating3 = rating3,
                id4 = name4,
                rating4 = rating4,
                id5 = name5,
                rating5 = rating5,
                id6 = name6,
                rating6 = rating6,
                id7 = name7,
                rating7 = rating7,
                id = username,
                )
    return redirect ("/submitted")



@app.route("/submitted", methods=["GET"])
def get_submitted():
    return render_template("/submitted.html")

@app.route("/results", methods=["GET"])
def get_results():
    #Each time the results page is loaded, runs the main() function of the algorithm, which returns a list of two elements.
    result = main()
    return render_template("/results.html", result = result)