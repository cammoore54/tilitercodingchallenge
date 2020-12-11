"""

    This applicaiton is for coding challenge 3.1. It uses a python flask server to serve a simple search bar applcation
"""


from flask import Flask, render_template, jsonify
import json
app = Flask(__name__)

@app.route('/')
def index():
    with open('data/movie_metadata.json') as jsonFile:
        movieData = json.load(jsonFile)
    #     movieData = {'movieData': movieData}
    with open('data/theater_showtimes.json') as jsonFile:
        showTimes = json.load(jsonFile)
        # showTimes = {'showTimes': showTimes}
    # movieData.update(showTimes)

    return render_template('index.html', movieData=movieData, showTimes=showTimes)

@app.route('/get-movie-data', methods = ['POST'])
def getMovieData():
    with open('data/movie_metadata.json') as jsonFile:
        movieData = json.load(jsonFile)
        movieData = {'movieData': movieData}
    with open('data/theater_showtimes.json') as jsonFile:
        showTimes = json.load(jsonFile)
        showTimes = {'showTimes': showTimes}
    movieData.update(showTimes)
    return jsonify(movieData)

app.run(debug=True,host='0.0.0.0')