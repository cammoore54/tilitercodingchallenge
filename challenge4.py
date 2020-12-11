import numpy as np
import cv2
import argparse





def changeResolution(frame, width, height):
    width = int(width)
    height = int(height)
    resolution = (width, height)
    return cv2.resize(frame, resolution, interpolation =cv2.INTER_AREA)


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main(filePath,frameRate,width,height,monochrome):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--videopath", required=False, default=filePath, help="Path to video file")
    ap.add_argument("-f", "--framerate", required=False, default=frameRate, help="Framerate for video playback")
    ap.add_argument("-w", "--width", required=False, default=width, type=int, help="Width of video")
    ap.add_argument("-hi", "--height", required=False, default=height, type=int, help="Height of video")
    # ap.add_argument("-r", "--resolution", required=False, default=resolution, help="Resolution of video")
    # ap.add_argument("-m", "--monochrome", required=False, default=monochrome, help="'True' for monochrome, 'False' for colour")
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

    cap = cv2.VideoCapture('videos/video_1.mp4')
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
        print(ord('q'))

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