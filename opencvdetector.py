###############################################################################
#  Program Name   : Apriltag Project
#  Author         : Yazan Elliethy
#  Date           : 2025-09-22
#  Class/Section  : ICS3U, Section 01
#  Description    : This program takes an input from a camera, then scans for
# april tag position.
#  Input          : Webacm.
#  Output         : Print apriltag location and orientation to
#  window of camera stream.
###############################################################################

from pyapriltags import Detector
from PIL import Image
import numpy
import cv2
from numpy import pi
import euler
import math
import keyboard

# Open camera
cap = cv2.VideoCapture(0)

tagSizeFloat = 0.15
promptText = ""
inPromptResize = False

keyboard.add_hotkey('v', lambda: print('V was pressed'))
keyboard.add_hotkey('m', lambda: print('M was pressed'))
keyboard.add_hotkey('space', lambda: print('Space was pressed'))

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Capture and process each frame

with open("log.txt", "r+") as f:
    data = f.read()
    f.seek(0)
    f.write("")
    f.truncate()

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame.")
        break

    # Display the frame
    cv2.imwrite('detected.png', frame)

    img = Image.open('detected.png').convert("L")
    numpyImg = numpy.array(img, dtype=numpy.uint8)

    detector = Detector(
                        families='tag36h11',
                        nthreads=1,
                        quad_decimate=1.0,
                        quad_sigma=0.0,
                        refine_edges=1,
                        decode_sharpening=0.25,
                        debug=0)

    tags = detector.detect(
        numpyImg, estimate_tag_pose=True, 
        camera_params=[526.0, 468.0, 640.0, 480.0], 
        tag_size=tagSizeFloat
    )

    if tags:
        distText = f"Dist: X: {tags[0].pose_t[0]*100}, Y: {tags[0].pose_t[1]*100}, Z: {tags[0].pose_t[2]*100}"
        a, b, c = euler.angles("xyz", tags[0].pose_R)
        rotText = f"Rot: X: {round(a*(180/math.pi), 2)}, "
        rotText = rotText + f"Y: {round(b*(180/math.pi), 2)}, "
        rotText = rotText + f"Z: {round(c*(180/math.pi), 2)}"
        corners = f"{tags[0].corners[0]}"
        print(f"TAG!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{corners.split(' ')[0]}")
    else:
        distText="Dist: N/A"
        rotText = "Rot: N/A"
    print(tags)
    with open('log.txt', 'a') as f:
        f.write("\n"+distText+"\n"+rotText)

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = 00, 185
    orgTwo = 00, 145
    orgThree = 30, 50
    orgFour = 30, 400
    fontScale = 0.5
    color = (0, 0, 255)
    thickness = 1

    distTextImg = cv2.putText(frame, 
        distText, 
        org, 
        font, 
        fontScale, 
        color, 
        thickness, 
        cv2.LINE_AA, 
        False
    )

    rotTextImg = cv2.putText(distTextImg, 
        rotText, 
        orgTwo, 
        font, 
        fontScale, 
        color, 
        thickness, 
        cv2.LINE_AA, 
        False
    ) 

    scaleImg = cv2.putText(rotTextImg, 
        str(tagSizeFloat), 
        orgFour, 
        font, 
        fontScale, 
        color, 
        thickness, 
        cv2.LINE_AA, 
        False
    )

    thickness = 2

    if tags:
        startPointY = tuple(tags[0].corners[0].astype(int))
        endPointY = tuple(tags[0].corners[3].astype(int))
        colorY = (0, 255, 0)
        imageWithY = cv2.line(scaleImg, startPointY, endPointY, colorY, thickness)
        startPointX = tuple(tags[0].corners[0].astype(int))
        endPointX = tuple(tags[0].corners[1].astype(int))
        colorX = (0, 0, 255)
        imageWithX = cv2.line(imageWithY, startPointX, endPointX, colorX, thickness)
    else:
        imageWithX = scaleImg

    if keyboard.is_pressed("space"):
        inPromptResize = True
        promptText = "Hold camera 30cm away from apriltag, then press v. To cancel, press m."
        
    
    if keyboard.is_pressed("m"):
        inPromptResize = False
        promptText = ""
    
    if keyboard.is_pressed("v"):
        if(inPromptResize):
            tagSizeFloat = float(0.15*(30/(tags[0].pose_t[2]*100)))
            promptText = ""
            inPromptResize = False

    readyImg = cv2.putText(imageWithX, 
        promptText, 
        orgThree, 
        font, 
        fontScale, 
        color, 
        thickness, 
        cv2.LINE_AA, 
        False
    ) 

    cv2.imshow('Webcam Feed', readyImg)

    

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()