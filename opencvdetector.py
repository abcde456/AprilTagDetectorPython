from pupil_apriltags import Detector
from PIL import Image
import numpy
import cv2

img = cv2.imread()
img = img.convert("L")
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

print(tags)