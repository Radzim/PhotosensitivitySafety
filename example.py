from PhotosensitivitySafetyEngine.PhotosensitivitySafetyEngine.guidelines.w3c import *
from PhotosensitivitySafetyEngine.PhotosensitivitySafetyEngine.video_tools.video_censor import *

# TO ANALYSE FILE
w3c_guideline.analyse_file('Pokemon.mp4')
w3c_guideline.analyse_file('Pokemon.mp4', display=Display(display_resolution=(1024, 768), display_diameter=16, display_distance=24))

# TO ANALYSE LIVE CAPTURE
w3c_guideline.analyse_live(speedup=10)

# TO CENSOR A VIDEO
safe, result = w3c_guideline.analyse_file('Pokemon.mp4', show_live_analysis=False, show_live_chart=False)
if not safe:
    video_censor('Pokemon.mp4', analysis_result=result, fallback_frames=6)
