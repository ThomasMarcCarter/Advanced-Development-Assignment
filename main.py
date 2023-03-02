import logging
from flask import Flask, render_template, request, redirect
import datetime
from google.auth.transport import requests as grequests
from google.cloud import datastore
import google.oauth2.id_token
import requests
from pymongo import MongoClient
from bson.json_util import dumps
from flask import Blueprint, request, jsonify
import os
import requests
import json
import pymongo
from pymongo import MongoClient

firebase_request_adapter = grequests.Request()

datastore_client = datastore.Client()

app = Flask(__name__)

mongoClient = MongoClient(
    "mongodb+srv://tc1301:Superses2@cluster0.nrl5wjb.mongodb.net/?retryWrites=true&w=majority"
)
mongoDB = mongoClient["ADUnit"]


def add_game_mongodb(gameTitle, coverArt, price):
    collection = mongoDB["Games"]
    json_data = {"gameTitle": gameTitle, "coverArt": coverArt, "price": price}
    collection.insert_one(json_data)


@app.route("/")
@app.route("/home")
def home():
    url = "https://europe-west2-ad-project-afc20.cloudfunctions.net/getmongoitems"
    response = requests.get(url)
    jresponse = response.text
    jsondata = json.loads(jresponse)
    for gameTitle in jsondata:
        for key, value in gameTitle.items():
            print(key, value)
    return render_template("home.html", jsondata=jsondata)


@app.route("/addgame", methods=["POST"])
def addgame():
    gameTitle = request.form["gameTitle"]
    coverArt = request.form["coverArt"]
    price = request.form["price"]

    if gameTitle and coverArt and price:
        add_game_mongodb(gameTitle, coverArt, price)
    return redirect("/")


def delete_post_mongodb(gameTitle):
    collection = mongoDB["Games"]
    jsonData = {"gameTitle": gameTitle}
    collection.delete_one(jsonData)


@app.route("/deletegame", methods=["POST"])
def deletePost():
    gameTitle = request.form["gameTitle"]

    if gameTitle:
        delete_post_mongodb(gameTitle)
    return redirect("/home")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register")
def form():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/cart")
def cart():
    return render_template("cart.html")


@app.route("/upload")
def upload():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None

    if id_token:
        try:
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load. For improved performance,
            # some applications may wish to cache results in an encrypted
            # session store (see for instance
            # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter
            )

        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)
    
    return render_template("upload.html", user_data=claims, error_message=error_message)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception("An error occurred during a request.")
    return "An internal error occurred.", 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    # Only run for local development.
    app.run(host="127.0.0.1", port=8080, debug=True)
