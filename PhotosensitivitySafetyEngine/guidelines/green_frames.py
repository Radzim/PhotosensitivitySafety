from GitHub.PhotosensitivitySafetyEngine.engine.analysis import GuidelineProcess, Display
from GitHub.PhotosensitivitySafetyEngine.engine.function_type_objects import *
from GitHub.PhotosensitivitySafetyEngine.libraries import common_functions
import numpy as np

# FUNCTION OBJECTS
function_objects = lambda properties: {
    'colorCurve': common_functions.colorCurve('RGB2XYZ'),
    'greenValue': common_functions.colorValue(green=1),
    'greenProportion': common_functions.colorProportion(green=1),
    'valueThreshold': common_functions.threshold(0.3),
    'proportionThreshold': common_functions.threshold(0.5),
    'greenFrameFragments': common_functions.twoConditions(),
    'greenFrameProportion': ArrayToValue(lambda x: np.average(x)),
    'greenFrameAlert': ValueToValue(lambda x: x>0.03),
    'countGreenFrames': ValueHistoryToValue(lambda x: sum(x))
}

# PROCESSING PIPELINE
processing_pipeline = [
    ('colorCurve', 0),
    ('greenValue', 1),
    ('greenProportion', 1),
    ('valueThreshold', 2),
    ('proportionThreshold', 3),
    ('greenFrameFragments', (4, 5)),
    ('greenFrameProportion', 6, "Green%"),
    ('greenFrameAlert', 7, "Too Green"),
    ('countGreenFrames', 8, "Total Too Green Frames")
]

# GUIDELINE OBJECT CREATION
w3c_guideline = GuidelineProcess(function_objects, processing_pipeline)
display_properties = Display(display_resolution=(1024, 768), display_diameter=16, display_distance=24)
w3c_guideline.analyse('C:/Users/radzi/OneDrive/Desktop/II/Project/MediaOut/video.avi', display_properties, speedup=5)
