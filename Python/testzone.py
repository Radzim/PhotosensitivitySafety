from frame_functions import *
from help_functions import *
import numpy as np

testArray = np.loadtxt('array.txt')

display_content(testArray)

cv2.waitKey(1000000)
