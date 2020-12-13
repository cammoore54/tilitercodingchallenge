import cv2
import argparse
import os


def backgroundSubtractionModel(frame,backSub):
    fgMask = backSub.apply(frame)
    fgMask = cv2.medianBlur(fgMask,7)
    bitwiseAnd = cv2.bitwise_and(frame, frame, mask=fgMask)
    
    return bitwiseAnd

def absDiffSubtraction(frame,firstFrame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)
    # In each iteration, calculate absolute difference between current frame and reference frame
    difference = cv2.absdiff(blurred, firstFrame)
    # Apply thresholding to eliminate noise
    thresh = cv2.threshold(difference, 70, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    bitwiseAnd = cv2.bitwise_and(frame, frame, mask=thresh)

    return bitwiseAnd

def processVideo(config, algorithm):

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

    frameWidth = int(cap.get(3))
    frameHeight = int(cap.get(4))
    frameRate = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(config["processedFilePath"]+config["resizeProcessedFileName"],fourcc, frameRate, (frameWidth,frameHeight))
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if algorithm == 'MOG2' or algorithm == 'KNN':
            processedFrame = backgroundSubtractionModel(frame,backSub)
        else:
            processedFrame = absDiffSubtraction(frame,firstFrame)
        out.write(processedFrame)

    cap.release()
    out.release()


def main(filePath):
    ap = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV.')
    ap.add_argument("-v", "--videopath", required=False, default=filePath, help="Path to video file")
    ap.add_argument("-a", "--algorithm", type=str, help='Background subtraction method (KNN, MOG2, ABSDIFF).', default='MOG2')

    args = vars(ap.parse_args())
    if "videopath" in args:
        filePath = args['videopath']
    if "algorithm" in args:
        algorithm = args['algorithm']

    cap = cv2.VideoCapture(filePath)
    # cap.set(cv2.CAP_PROP_POS_FRAMES, 105)

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
    
    rootDir = os.path.dirname(filePath)
    fileName=os.path.basename(filePath)
    processedFileName = os.path.splitext(fileName)[0] + "_processed.mp4"
    processedFileName = os.path.join(rootDir, processedFileName)
    frameWidth = int(cap.get(3))
    frameHeight = int(cap.get(4))
    frameRate = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(processedFileName,fourcc, frameRate, (frameWidth,frameHeight))
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if algorithm == 'MOG2' or algorithm == 'KNN':
            processedFrame = backgroundSubtractionModel(frame,backSub)
        else:
            processedFrame = absDiffSubtraction(frame,firstFrame)
        out.write(processedFrame)
    cap.release()
    out.release()




if __name__ == '__main__':
    filePath = '../videos/video_1.mp4'
    main(filePath)