from GitHub.generalisation.libraries import custom_functions
from GitHub.generalisation.libraries import common_functions

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
bothConditions = common_functions.twoConditions()
redSaturation = ArrayToArrayChannels(lambda R, G, B: np.maximum(R - G - B, 0) * 320, vector_form=True)
maximumRegion = ArrayToValue(lambda x: custom_functions.area_averages_max(x, threshold=0.25))
full_flash_count = lambda x, y: custom_functions.count_flashes(x, y, frame_rate=30)


# PROCESSING PIPELINE
def processingPipeline(video_frame, register_values):
    cc = colorCurve.run(video_frame)
    rl = relativeLuminance.run(cc)
    rll = relativeLuminanceLighter.run(rl)
    rld = relativeLuminanceDarker.run(rl)
    rlc = relativeLuminanceCondition.run(rl)
    rldc = bothConditions.run(rll, rlc)
    rllc = bothConditions.run(rld, rlc)
    rp = redProportion.run(cc)
    rs = redSaturation.run(cc)
    rsu = redSaturationChangeUp.run(rs)
    rsd = redSaturationChangeDown.run(rs)
    rpc = redProportionCondition.run(rp)
    rsuc = bothConditions.run(rsu, rpc)
    rsdc = bothConditions.run(rsd, rpc)
    register_values.add('general_flash_up', maximumRegion.run(rldc))
    register_values.add('general_flash_down', maximumRegion.run(rllc))
    register_values.add('red_flash_up', maximumRegion.run(rsuc))
    register_values.add('red_flash_down', maximumRegion.run(rsdc))
    register_values.add('general_flash_count', full_flash_count(register_values.get('general_flash_up'), register_values.get('general_flash_down')))
    register_values.add('red_flash_count', full_flash_count(register_values.get('red_flash_up'), register_values.get('red_flash_down')))


analyse('C:/Users/radzi/OneDrive/Desktop/II/Project/MediaOut/video.avi')

