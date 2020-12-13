"""
    Includes all functions to complete challenge 4.1

    Modules used:
    cv2: opencv - for image processing
    argparse: commandline arguments from user
"""

import cv2
import argparse

def changeResolution(frame, width, height):
    """
        Changes resolution of frame
    Args: 
        frame: frame to process
        width: desired new width
        hight: desired new height
    Returns: Resized frame

    """
    width = int(width)
    height = int(height)
    resolution = (width, height)
    return cv2.resize(frame, resolution, interpolation=cv2.INTER_AREA)


def str2bool(v):
    """
        Takes all interpretaions of 'true' and converts to boolean
    Args:
        v: value from user
    Returns: 
        BOOL
    """
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def saveFile(config,frameRate=10,frameWidth=False,frameHeight=False,colour=True):
    """
        Saves video file with new configuration
    Args:
        config: system config file
        frameRate: desired framerate
        frameWidth: desired frame width
        frameHeight: desired frame height
        colour: colour = True, grayscale = False

    """
    # Read video file
    cap = cv2.VideoCapture(config['tempUploadPath'])
    # Set parameters
    keepOriginalRes = False
    if not frameWidth and not frameHeight:
        keepOriginalRes = True
    if not frameWidth:
        frameWidth = int(cap.get(3))
    if not frameHeight:
        frameHeight = int(cap.get(4))

    # Initialise writer object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")    #Required to write mp4 files
    out = cv2.VideoWriter(config["processedFilePath"]+config["processedFileName"],fourcc, frameRate, (frameWidth,frameHeight))

    # Loop through each frame, process it and write to file
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
    # Cleanup
    cap.release()
    out.release()


def main(filePath,frameRate,width,height,monochrome):
    """
        Takes commandline arguments or script arguments from user and displays configured video
    Args:
        filePath: path to video file
        frameRate: desired viewing frame rate
        width: desired frame width
        height: desired frame height
        monochrome: True = grayscale, False = colour
    """

    # Parse commandline arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--videopath", required=False, default=filePath, help="Path to video file")
    ap.add_argument("-f", "--framerate", required=False, default=frameRate, type=int, help="Framerate for video playback")
    ap.add_argument("-w", "--width", required=False, default=width, type=int, help="Width of video")
    ap.add_argument("-hi", "--height", required=False, default=height, type=int, help="Height of video")
    ap.add_argument("-m", "--monochrome", type=str2bool, default=monochrome, help="True' for monochrome, 'False' for colour")
    
    args = vars(ap.parse_args())
    # If commandline arguments are specified use them, otherwise use script arguments
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

    # create capture object
    cap = cv2.VideoCapture(filePath)
    # Delay = 1000ms/frameRate
    delay = int(1000/frameRate)
    while(True):
        ret, frame = cap.read()
        if not ret:
            break
        # Resize frame
        resizedFrame = changeResolution(frame,width,height)

        # Convert to monochrome
        if monochrome:
            gray = cv2.cvtColor(resizedFrame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame',gray)
        else:
            cv2.imshow('frame',resizedFrame)

        breakLoop= False
        # Get key input from user
        keyPressed = cv2.waitKey(delay) 

        # cv2.waitkey returns 32 bit number, we only care about the last 8 bits
        # if p is pressed
        if keyPressed & 0xFF == ord('p'):
            while not breakLoop:
                # Check if any other keys are pressed while paused
                keyPressed = cv2.waitKey(1)
                # if b is pressed
                if keyPressed & 0xFF == ord('b'):
                    # Get next frame
                    nextFrame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                    # Set it back two 
                    cap.set(cv2.CAP_PROP_POS_FRAMES, nextFrame-2)
                    ret, frame = cap.read()
                    resizedFrame = changeResolution(frame,width,height)
                    if monochrome:
                        gray = cv2.cvtColor(resizedFrame, cv2.COLOR_BGR2GRAY)
                        cv2.imshow('frame',gray)
                    else:
                        cv2.imshow('frame',resizedFrame)
                # if 'p' is pressed, continue
                elif keyPressed & 0xFF == ord('p'):
                    breakLoop = True
        # if q is pressed, quit
        elif keyPressed & 0xFF == ord('q'):
            break
    
    # cleanup
    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    filePath = 'videos/video_1.mp4'
    frameRate = 20
    width = 400
    height = 200
    monochrome = True
    main(filePath,frameRate,width,height,monochrome)