from PhotosensitivitySafetyEngine.PhotosensitivitySafetyEngine.engine.analysis import GuidelineProcess, Display
from PhotosensitivitySafetyEngine.PhotosensitivitySafetyEngine.libraries.function_objects import *
from PhotosensitivitySafetyEngine.PhotosensitivitySafetyEngine.libraries import common_functions, custom_functions
from PhotosensitivitySafetyEngine.PhotosensitivitySafetyEngine.video_tools.video_censor import *
import numpy as np

# FUNCTION OBJECTS
function_objects = lambda properties: {
    'colorCurve': common_functions.colorCurve('RGB2XYZ'),
    'relativeLuminance': common_functions.relativeLuminance(),
    'relativeLuminanceLighter': common_functions.changeDetect(direction=1, minimum=20/properties['candelas']),
    'relativeLuminanceDarker': common_functions.changeDetect(direction=-1, minimum=20/properties['candelas']),
    'relativeLuminanceCondition': common_functions.pastOrPresentThreshold(160/properties['candelas'], direction=-1),
    'bothConditions': common_functions.twoConditions(),
    'combinedAreaCondition': ArrayToValue(lambda x: np.average(x) > 0.25),
    'fullFlashCountGeneral': ValueHistoriesToValue(lambda x, y: custom_functions.count_flashes(x, y, frame_rate=properties['frame_rate'])),
    'threshold': ValueToValue(lambda x: x > 3)
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
    ('combinedAreaCondition', 6),
    ('combinedAreaCondition', 7),
    ('fullFlashCountGeneral', (8, 9), "General Flashes"),
    ('threshold', 10, "Fail")
]

# GUIDELINE OBJECT CREATION
ofcom_guideline = GuidelineProcess(function_objects, processing_pipeline)

display = Display(display_resolution=(1024, 768), display_diameter=16, display_distance=24)

path = 'C:/Users/radzi/OneDrive/Desktop/II/Project/MediaOut/video.avi'
result, breaches = ofcom_guideline.analyse_file(path, display=display, speedup=3, show_live_analysis=False, show_live_chart=False)
print(result)
video_censor(path, breaches, fallback_frames=6, frames_before=30)

path = 'C:/Users/radzi/OneDrive/Desktop/II/Project/MediaOut/video_censored.avi'
result, _ = ofcom_guideline.analyse_file(path, display=display, speedup=3, show_live_analysis=False, show_live_chart=False)
print(result)
