from PhotosensitivitySafetyEngine.PhotosensitivitySafetyEngine.engine.analysis import GuidelineProcess, Display
from PhotosensitivitySafetyEngine.PhotosensitivitySafetyEngine.libraries.function_objects import *
from PhotosensitivitySafetyEngine.PhotosensitivitySafetyEngine.libraries import common_functions, custom_functions
from PhotosensitivitySafetyEngine.PhotosensitivitySafetyEngine.video_tools.video_censor import *
import numpy as np

# FUNCTION OBJECTS

function_objects = lambda properties: {
    'colorCurve': common_functions.colorCurve('RGB2XYZ'),
    'relativeLuminance': common_functions.relativeLuminance(),
    'relativeLuminanceLighter': common_functions.changeDetect(direction=1, minimum=0.1),
    'relativeLuminanceDarker': common_functions.changeDetect(direction=-1, minimum=0.1),
    'redSaturationChangeUp': common_functions.changeDetect(direction=1, minimum=20),
    'redSaturationChangeDown': common_functions.changeDetect(direction=-1, minimum=20),
    'relativeLuminanceCondition': common_functions.pastOrPresentThreshold(0.8, direction=-1),
    'redProportionCondition': common_functions.pastOrPresentThreshold(0.8, direction=1),
    'redProportion': common_functions.colorProportion(red=1),
    'bothConditions': common_functions.twoConditions(),
    'redSaturation': ArrayToArrayChannels(lambda R, G, B: np.maximum(R - G - B, 0) * 320, vector_form=True),
    'maximumRegion': ArrayToValue(lambda x: custom_functions.area_averages_max(x, fragment_shape=properties['degree_field'](10), threshold=0.25)),
    'fullFlashCountGeneral': ValueHistoriesToValue(lambda x, y: custom_functions.count_flashes(x, y, frame_rate=properties['frame_rate'])),
    'fullFlashCountRed': ValueHistoriesToValue(lambda x, y: custom_functions.count_flashes(x, y, frame_rate=properties['frame_rate'])),
    'eitherThreshold': ValuesToValue(lambda x, y: x > 3 or y > 3)
}

# PROCESSING PIPELINE
processing_pipeline = [
    ('colorCurve', 0),
    ('relativeLuminance', 1),
    ('relativeLuminanceLighter', 2),
    ('relativeLuminanceDarker', 2),
    ('relativeLuminanceCondition', 2),
    ('bothConditions', (3, 5)),
    ('bothConditions', (4, 5)),
    ('redProportion', 1),
    ('redSaturation', 1),
    ('redSaturationChangeUp', 9),
    ('redSaturationChangeDown', 9),
    ('redProportionCondition', 8),
    ('bothConditions', (10, 12)),
    ('bothConditions', (11, 12)),
    ('maximumRegion', 6),
    ('maximumRegion', 7),
    ('maximumRegion', 13),
    ('maximumRegion', 14),
    ('fullFlashCountGeneral', (15, 16), "General Flashes"),
    ('fullFlashCountRed', (17, 18), "Red Flashes"),
    ('eitherThreshold', (19, 20), "Fail")
]

# GUIDELINE OBJECT CREATION
w3c_guideline = GuidelineProcess(function_objects, processing_pipeline)

# display = Display(display_resolution=(1024, 768), display_diameter=16, display_distance=24)
#
# path = 'C:/Users/radzi/OneDrive/Desktop/II/Project/MediaOut/video.avi'
# result, breaches = w3c_guideline.analyse_file(path, display=display, speedup=3, show_live_analysis=False, show_live_chart=False)
# print(result)
# video_censor(path, breaches, fallback_frames=6, frames_before=30)
#
# path = 'C:/Users/radzi/OneDrive/Desktop/II/Project/MediaOut/video_censored.avi'
# result, _ = w3c_guideline.analyse_file(path, display=display, speedup=3, show_live_analysis=False, show_live_chart=False)
# print(result)
