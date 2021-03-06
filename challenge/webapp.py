"""
    This applicaiton is for coding challenge 3.1. It uses a python flask server to serve a simple web app
    that allows user to search for the session times of a movie, based on the theatre and movie title.

    The path to the json files are in config.json

    Modules used:
    flask: Webserver
    json: parse movie data
    werkzeug.utils: Stops malicious filenames
    os: OS functions
    sys: system functions
    challenge4: video processing functions
"""

from flask import Flask, render_template, jsonify, request, send_from_directory, url_for, abort
from werkzeug.utils import secure_filename  
import json
import os
import sys
sys.path.insert(0,'..')
from challenge4 import challenge4_1, challenge4_2
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

@app.route('/video-processing')
def videoProcessing():
    """ Route for challenges 4.1 and 4.2

    '"""
    return render_template('video-processing.html')

@app.route('/resize-video', methods=['POST'])
def resideVideo():
    """ Gets file and data from client configures the framerate, resolution and colour

    """

    # Parse data from client
    uploadedFile = request.files['file']
    frameWidth = request.form['frameWidth']
    if frameWidth == '':
        frameWidth = False
    else:
        frameWidth = int(frameWidth)
    frameHeight = request.form['frameHeight']
    if frameHeight == '':
        frameHeight = False
    else:
        frameHeight = int(frameHeight)
    frameRate = request.form['frameRate']
    if frameRate == '':
        frameRate = 5
    else:
        frameRate = int(frameRate)
    colour = request.form['colour']
    if colour == 'true':
        colour = True
    else:
        colour = False
    
    # Extract the filename safely
    filename = secure_filename(uploadedFile.filename)
    attachmentFileName = os.path.splitext(filename)[0] + "_processed.mp4"
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in config['uploadExtensions']:
            return jsonify({"status": "fail"})
        # Save uploaded file to a temp location
        uploadedFile.save(config['tempUploadPath'])
        # Process the video
        challenge4_1.saveFile(config,frameRate,frameWidth,frameHeight,colour)
    else:
        return jsonify({"status": "fail"})
    
    return jsonify({"status": "success", "path": url_for('downloadFile', fileName=config["processedFileName"], attachmentName = attachmentFileName)})


@app.route('/background-removal', methods=['POST'])
def backgroundRemoval():
    """ Removes background from video

    """
    # Parse data from client
    uploadedFile = request.files['file']
    algorithm = request.form['algorithm']
    filename = secure_filename(uploadedFile.filename)
    attachmentFileName = os.path.splitext(filename)[0] + "_processed.mp4"
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in config['uploadExtensions']:
            return jsonify({"status": "fail"})
        uploadedFile.save(config['tempUploadPath'])
        # Process the video
        challenge4_2.processVideo(config,algorithm)
    else:
        return jsonify({"status": "fail"})
    
    return jsonify({"status": "success", "path": url_for('downloadFile', fileName=config["processedFileName"], attachmentName = attachmentFileName)})


@app.route('/download_processed_video/<path:fileName>/<path:attachmentName>')
def downloadFile(fileName,attachmentName):
    """ Route to get file from file system and make available to client

    """

    filePath = config["processedFilePath"]
    return send_from_directory(filePath, fileName, as_attachment=True, mimetype='video/x-msvideo', attachment_filename=attachmentName)

# Start application
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')