import time

import pandas as pd
from matplotlib import pyplot as plt

from GitHub.Python.generalisation.lambdas import *
from GitHub.Python.generalisation.libraries import common_functions, custom

import re
def count_flashes(flashes_lighter, flashes_darker, frame_rate):
    # this may be over-counting slightly
    flashes_lighter[0], flashes_darker[0] = 0, 0
    channel1, channel2 = flashes_lighter[-(frame_rate - 1):], flashes_darker[-(frame_rate - 1):]
    both_channels = ''
    for i in range(len(channel1)):
        if channel1[i] and channel2[i]:
            both_channels += 'X'
        elif channel1[i]:
            both_channels += '1'
        elif channel2[i]:
            both_channels += '2'
    both_channels = re.sub('1+', '1', both_channels)
    both_channels = re.sub('2+', '2', both_channels)
    count = len(both_channels)
    return count


general_flashes_lighter = []
general_flashes_darker = []
general_flashes_counter = []
red_flashes_lighter = []
red_flashes_darker = []
red_flashes_counter = []


# FUNCTIONS USED
colorCurve = common_functions.colorCurve('RGB2XYZ')
relativeLuminance = common_functions.relativeLuminance()
relativeLuminanceLighter = common_functions.changeDetect(direction=1, minimum=0.1)
relativeLuminanceDarker = common_functions.changeDetect(direction=-1, minimum=0.1)
redSaturationChangeUp = common_functions.changeDetect(direction=1, minimum=20)
redSaturationChangeDown = common_functions.changeDetect(direction=-1, minimum=20)
relativeLuminanceCondition = common_functions.pastOrPresentThreshold(0.8, direction=-1)
redProportionCondition = common_functions.pastOrPresentThreshold(0.8, direction=1)
redProportion = common_functions.colorProportion(red=1)
redSaturation = ArrayToArrayChannels(lambda R, G, B: np.maximum(R - G - B, 0) * 320, vector_form=True)
maximumRegion = ArrayToBoolean(lambda x: custom.area_averages_max(x, threshold=0.25))
bothConditions = common_functions.twoConditions()

# REGISTERS
general_flashes_up = Register()
general_flashes_down = Register()
red_flashes_up = Register()
red_flashes_down = Register()

# PROCESSING PIPELINE
def processingPipeline(frame):
    cc = colorCurve.run(frame)
    rl = relativeLuminance.run(cc)
    rll = relativeLuminanceLighter.run(rl)
    rld = relativeLuminanceDarker.run(rl)
    rlc = relativeLuminanceCondition.run(rl)
    rldc = bothConditions.run(rll, rlc)
    rllc = bothConditions.run(rld, rlc)
    rldcx = maximumRegion.run(rldc)
    rllcx = maximumRegion.run(rllc)
    rp = redProportion.run(cc)
    rs = redSaturation.run(cc)
    rsu = redSaturationChangeUp.run(rs)
    rsd = redSaturationChangeDown.run(rs)
    rpc = redProportionCondition.run(rp)
    rsuc = bothConditions.run(rsu, rpc)
    rsdc = bothConditions.run(rsd, rpc)
    rsucx = maximumRegion.run(rsuc)
    rsdcx = maximumRegion.run(rsdc)


    general_flashes_lighter.append(int(stage_01235))
    general_flashes_darker.append(int(stage_01245))
    general_flashes_counter.append(count_flashes(general_flashes_lighter, general_flashes_darker, 30))

    red_flashes_lighter.append(int(stage_07A_068_5))
    red_flashes_darker.append(int(stage_07A_069_5))
    red_flashes_counter.append(count_flashes(red_flashes_lighter, red_flashes_darker, 30))

    return [stage_01235, stage_01245, stage_07A_068_5, stage_07A_069_5]


# Dataframe
df = pd.DataFrame(columns=['Lighter', 'Darker', 'More-Red', 'Less-Red'])

capture = cv2.VideoCapture('C:/Users/radzi/OneDrive/Desktop/II/Project/MediaOut/video.avi')
print(time.time())
for i in range(333):
    print(i)
    check, frame = capture.read()
    df.loc[i] = processingPipeline(frame)
print(time.time())
print(df.T.astype(int).to_string())

plt.plot(np.arange(len(general_flashes_counter)) / 30, general_flashes_counter)
plt.plot(np.arange(len(general_flashes_counter)) / 30, red_flashes_counter)
plt.plot(np.arange(len(general_flashes_counter)) / 30, [3] * len(general_flashes_counter))
plt.ylabel('Flash Counts')
plt.show()

