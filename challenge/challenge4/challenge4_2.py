"""
    Includes all functions to complete challenge 4.2

    Modules used:
    cv2: opencv - for image processing
    argparse: commandline arguments from user
    os: path manipulation 
    json: parse config
"""

import cv2
import argparse
import os
import json

def backgroundSubtractionModel(frame,backSub):
    """
        Performs opencv background subtraction
    Args:
        frame: frame to process
        backSub: background subtraction model
    Returns: 
        Segmented frame
    """
    fgMask = backSub.apply(frame)
    fgMask = cv2.medianBlur(fgMask,7)
    bitwiseAnd = cv2.bitwise_and(frame, frame, mask=fgMask)
    
    return bitwiseAnd

def absDiffSubtraction(frame,firstFrame):
    """
        Performs background subtraction based on absolute difference between initial frame and current frame
    Args:
        firstFrame: First frame of video
    Returns: 
        Segmented frame
    """
    # convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur to smooth 
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)
    # In each iteration, calculate absolute difference between current frame and reference frame
    difference = cv2.absdiff(blurred, firstFrame)
    # Apply thresholding to eliminate noise
    thresh = cv2.threshold(difference, 70, 255, cv2.THRESH_BINARY)[1]
    # dilute to further remove noise
    thresh = cv2.dilate(thresh, None, iterations=2)
    # extract frame from mask
    bitwiseAnd = cv2.bitwise_and(frame, frame, mask=thresh)

    return bitwiseAnd

def processVideo(config, algorithm, filePath=False):
    """
        Process video file
    Args:
        config: system config
        algorithm: background subtraction algorithm
    """
    cap = cv2.VideoCapture(config['tempUploadPath'])

    if algorithm == 'MOG2':
        backSub = cv2.createBackgroundSubtractorMOG2()
    elif algorithm == 'KNN':
        backSub = cv2.createBackgroundSubtractorKNN()
    elif algorithm == 'ABSDIFF':
        # Save the first image as reference
        ret, first = cap.read()
        firstFrame = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
        firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)
    else:
        print("Unknown background subtraction model")
        return

    # Get frame parameters
    frameWidth = int(cap.get(3))
    frameHeight = int(cap.get(4))
    frameRate = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")    #Required to write mp4 files
    if filePath:
        out = cv2.VideoWriter(filePath,fourcc, frameRate, (frameWidth,frameHeight))
    else:
        out = cv2.VideoWriter(config["processedFilePath"]+config["processedFileName"],fourcc, frameRate, (frameWidth,frameHeight))
    
    # Loop through frames and proccess
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if algorithm == 'MOG2' or algorithm == 'KNN':
            processedFrame = backgroundSubtractionModel(frame,backSub)
        else:
            processedFrame = absDiffSubtraction(frame,firstFrame)
        out.write(processedFrame)

    # Cleanup
    cap.release()
    out.release()


def fileNameConstructor(inputFilePath):
    """
        Appends '_processed' to filename
    Args:
        inputFilePath - file path to alter
    """
    rootDir = os.path.dirname(inputFilePath)
    fileName=os.path.basename(inputFilePath)
    processedFileName = os.path.splitext(fileName)[0] + "_processed.mp4"
    processedFilePath = os.path.join(rootDir, processedFileName)

    return processedFilePath


def main(inputFilePath):
    ap = argparse.ArgumentParser(description='This application performs background subtraction using opencv')
    ap.add_argument("-i", "--inputvideopath", required=False, default=inputFilePath, help="Path to input video file")
    ap.add_argument("-o", "--outputvideopath", required=False, default=fileNameConstructor(inputFilePath), help="Path to output video file")
    ap.add_argument("-a", "--algorithm", type=str, help='Background subtraction method (KNN, MOG2, ABSDIFF).', default='MOG2')

    args = vars(ap.parse_args())
    if "inputvideopath" in args:
        inputFilePath = args['inputvideopath']
    if "algorithm" in args:
        algorithm = args['algorithm']
    if "outputvideopath" in args:
        outputFilePath = args['outputvideopath']
    else:
        outputFilePath = fileNameConstructor(inputFilePath)

    with open('config.json') as configFile:
        config = json.load(configFile)

    processVideo(config,algorithm,outputFilePath) 



if __name__ == '__main__':
    inputFilePath = '../videos/video_1.mp4'
    main(inputFilePath)