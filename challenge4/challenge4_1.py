import numpy as np
import cv2
import argparse
import time

def changeResolution(frame, width, height):
    width = int(width)
    height = int(height)
    resolution = (width, height)
    return cv2.resize(frame, resolution, interpolation=cv2.INTER_AREA)


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def saveFile(config,frameRate=10,frameWidth=False,frameHeight=False,colour=True):

    cap = cv2.VideoCapture(config['tempUploadPath'])
    keepOriginalRes = False
    if not frameWidth and not frameHeight:
        keepOriginalRes = True
    if not frameWidth:
        frameWidth = int(cap.get(3))
    if not frameHeight:
        frameHeight = int(cap.get(4))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(config["processedFilePath"]+config["resizeProcessedFileName"],fourcc, frameRate, (frameWidth,frameHeight))

    while(True):
        ret, frame = cap.read()
        if ret == True:
            if not keepOriginalRes:
                frame = changeResolution(frame,frameWidth,frameHeight)
            if not colour:
                # videowriter write grayscale files is only supported in windows so need to convert frame to grayscale then convert back to a three channel image to write to file
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            out.write(frame)
        # Break the loop
        else:
            break  

    cap.release()
    out.release()
    # time.sleep(10)


def main(filePath,frameRate,width,height,monochrome):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--videopath", required=False, default=filePath, help="Path to video file")
    ap.add_argument("-f", "--framerate", required=False, default=frameRate, type=int, help="Framerate for video playback")
    ap.add_argument("-w", "--width", required=False, default=width, type=int, help="Width of video")
    ap.add_argument("-hi", "--height", required=False, default=height, type=int, help="Height of video")
    ap.add_argument("-m", "--monochrome", type=str2bool, default=monochrome, help="True' for monochrome, 'False' for colour")
    
    args = vars(ap.parse_args())

    if "videopath" in args:
        filePath = args['videopath']
    if 'framerate' in args:
        frameRate = args['framerate']
    if 'width' in args:
        width = args['width']
    if 'height' in args:
        height = args['height']
    if 'monochrome' in args:
        monochrome = args['monochrome']

    cap = cv2.VideoCapture(filePath)
    delay = int(1000/frameRate)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break
        resizedFrame = changeResolution(frame,width,height)

        if monochrome:
            gray = cv2.cvtColor(resizedFrame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame',gray)
        else:
            cv2.imshow('frame',resizedFrame)

        breakLoop= False
        keyPressed = cv2.waitKey(delay) 
        if keyPressed & 0xFF == ord('p'):
            while not breakLoop:
                keyPressed = cv2.waitKey(1)
                if keyPressed & 0xFF == ord('b'):
                    currentFrame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, currentFrame-2)
                    ret, frame = cap.read()
                    resizedFrame = changeResolution(frame,width,height)
                    if monochrome:
                        gray = cv2.cvtColor(resizedFrame, cv2.COLOR_BGR2GRAY)
                        cv2.imshow('frame',gray)
                    else:
                        cv2.imshow('frame',resizedFrame)
                elif keyPressed & 0xFF == ord('p'):
                    breakLoop = True
        elif keyPressed & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    filePath = 'videos/video_1.mp4'
    frameRate = 20
    width = 400
    height = 200
    monochrome = True
    main(filePath,frameRate,width,height,monochrome)