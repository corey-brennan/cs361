# Author: Corey Brennan
# ONID: brennaco
# CS 361: Project


from google.cloud import datastore
from json2html import *
from urllib.parse import urlencode
from flask import Flask, redirect, url_for, render_template, request, flash, session
from helper_functions import calculate_article_health, calculate_article_health_threaded
import flask
import json
import logging
import requests
import random
import string


# Creating flask app and generating secret key
app = flask.Flask(__name__)
app.secret_key = ''.join(random.sample(string.ascii_lowercase, 20))

# Route to calculate article health and return working/non-working links
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == "POST":
        
        # Grabbing data
        if request.content_type == "application/json":
            content = request.get_json()

            urls = content['links']

            if type(urls) == str:
                urls = urls.split(', ')

        elif request.content_type in (
            "application/x-www-form-urlencoded",
            "multipart/form-data",
        ):
            urls = request.form['links'].split(', ')
        else:
            return (json.dumps({"Error":"Unsupported Media Type"}), 415)

        if request.content_type == "application/json":
            return (json.dumps(calculate_article_health_threaded(urls)))
        else:
            return render_template('links.html', articleLinks=calculate_article_health_threaded(urls))

    else:
        return ("Method not recognized")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)