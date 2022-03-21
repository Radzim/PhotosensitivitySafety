import time
import pandas as pd
from lambdas import *
from fun_library import relative, max color,

# Function Objects
rlCurve = InputToArray(lambda X: max(X / 255 / 12.92, ((X / 255 + 0.055) / 1.055) ** 2.4))
relativeLuminance = ArrayToArrayChannels(lambda R, G, B: 0.2126 * R + 0.7152 * G + 0.0722 + B, vector_form=True)
lighter = ArrayAndPastToArray(lambda Present, Past: ((Present - Past) >= 0.1) * (Past <= 0.8))
darker = ArrayAndPastToArray(lambda Present, Past: ((Present - Past) <= -0.1) * (Present <= 0.8))
maximumRegion = ArrayToBoolean(lambda x: custom.area_averages_max(x, threshold=0.25))
redSaturation = ArrayToArrayChannels(lambda R, G, B: R / (R + G + B) if R else 0)
redMajority = ArrayToArrayChannels(lambda R, G, B: max(R - G - B, 0) * 320)
redSaturationChangeUp = ArrayAndPastToArray(lambda Present, Past: Present - Past > 20)
redSaturationChangeDown = ArrayAndPastToArray(lambda Present, Past: Present - Past < -20)
redMajorityChange = ArrayAndPastToArray(lambda Present, Past: max(Present, Past) >= 0.8)
bothConditions = ArraysToArray(lambda Array1, Array2: Array1 * Array2)


def processingPipeline(stage_0):
    print(time.time())
    stage_01 = rlCurve.run(stage_0)
    print(time.time())
    stage_012 = relativeLuminance.run(stage_01)
    print(time.time())
    stage_0123 = lighter.run(stage_012)
    print(time.time())
    stage_0124 = darker.run(stage_012)
    print(time.time())
    stage_01235 = maximumRegion.run(stage_0123)
    print(time.time())
    stage_01245 = maximumRegion.run(stage_0124)
    print(time.time())
    stage_06 = redSaturation.run(stage_01)
    print(time.time())
    stage_07 = redMajority.run(stage_01)
    print(time.time())
    stage_068 = redSaturationChangeUp.run(stage_06)
    print(time.time())
    stage_069 = redSaturationChangeDown.run(stage_06)
    print(time.time())
    stage_07A = redMajorityChange.run(stage_07)
    print(time.time())
    stage_07A_068 = bothConditions.run(stage_07A, stage_068)
    print(time.time())
    stage_07A_069 = bothConditions.run(stage_07A, stage_069)
    print(time.time())
    stage_07A_068_5 = maximumRegion.run(stage_07A_068)
    print(time.time())
    stage_07A_069_5 = maximumRegion.run(stage_07A_069)
    print(time.time())
    return [stage_01235, stage_01245, stage_07A_068_5, stage_07A_069_5]


# Dataframe
df = pd.DataFrame(columns=['Lighter', 'Darker', 'More-Red', 'Less-Red'])

capture = cv2.VideoCapture('C:/Users/radzi/OneDrive/Desktop/II/Project/MediaOut/video.avi')
for i in range(30):
    check, frame = capture.read()
    df.loc[i] = processingPipeline(frame)
print(df)
