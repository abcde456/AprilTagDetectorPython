from pupil_apriltags import Detector
from PIL import Image
import numpy
import cv2

# Open the default webcam (usually device 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
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

    tags = detector.detect(numpyImg, estimate_tag_pose=True, camera_params=[2.0, 3.7, 320.0, 240.0], tag_size=15.0)

    text = "Text"
    print(tags)
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = 00, 185
    fontScale = 0.5
    color = (0, 0, 0)
    thickness = 2

    modifiedImg = cv2.putText(frame, text, org, font, fontScale, color, thickness, cv2.LINE_AA, True) 

    cv2.imshow('Webcam Feed', modifiedImg)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()