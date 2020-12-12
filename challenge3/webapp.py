"""
    This applicaiton is for coding challenge 3.1. It uses a python flask server to serve a simple web app
    that allows user to search for the session times of a movie, based on the theatre and movie title.

    The path to the json files are in config.json

    Modules used:
    flask: Webserver
    json: parse movie data
"""

from flask import Flask, render_template, jsonify
import json
app = Flask(__name__)

with open('config.json') as configFile:
    config = json.load(configFile)

@app.route('/')
def index():
    """ Default route when user visits web page
        Gets path of movie meta data json file config and renders template of index page

    Returns:
        html: index.html
    """
    with open(config["movieMetadataPath"]) as jsonFile:
        movieData = json.load(jsonFile)
    return render_template('index.html', movieData=movieData)

@app.route('/get-show-times/<theatre>', methods = ['POST'])
def getShowTimes(theatre):
    """ POST request route to get showtime list

    Returns:
        json: showtime list

    """
    with open(config["theatreShowtimesPath"]) as jsonFile:
        showTimeList = json.load(jsonFile)

    for theatreNames in showTimeList:
        if theatreNames["name"] == theatre:
            return jsonify(theatreNames["showtimes"])

# Start application
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')