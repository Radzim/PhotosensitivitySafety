import os

from cv2 import cv2
from pytube import YouTube
from pytube import Playlist
#
# playlist = Playlist('https://www.youtube.com/playlist?list=PLirAqAtl_h2r5g8xGajEwdXd3x1sZh8hC')
# print('Number Of Videos In playlist: %s' % len(playlist.video_urls))
#
# for i in range(20):
#     yt = playlist.videos[i]
#     print("Title: ", yt.title)
#     print("Number of views: ", yt.views)
#
#     video = yt.streams.get_highest_resolution()
#
#     print("Downloading...")
#     video.download(output_path="C:/Users/radzi/OneDrive/Desktop/II/Project/TestVideos")
#     os.rename("C:/Users/radzi/OneDrive/Desktop/II/Project/TestVideos/"+video.default_filename, "C:/Users/radzi/OneDrive/Desktop/II/Project/TestVideos/"+str(i+1)+". "+video.default_filename)
#     print("Download completed\n\n")

# import glob
#
# from PhotosensitivitySafetyEngine.PhotosensitivitySafetyEngine.video_tools import video_convert
#
# files = glob.glob("C:/Users/radzi/OneDrive/Desktop/II/Project/TestVideos/*")
# for file in files:
#     print(file)
#     video_convert.convert_to_peat(file)

# address_in = "C:/Users/radzi/OneDrive/Desktop/II/Project/TestVideos/Resolutions/Video1.avi"
# for j in range(8):
#     res = (int(1920/2*(j+1)), int(1080/2*(j+1)))
#     print(res)
#     address_out = os.path.splitext(address_in)[0]+"_"+str(j+1)+'K.avi'
#     writer = cv2.VideoWriter(address_out, 0, 30, res)
#     capture = cv2.VideoCapture(address_in)
#     for i in range(900):
#         check, frame = capture.read()
#         if not check:
#             break
#         frame2 = cv2.resize(frame, res)
#         writer.write(frame2)
#     writer.release()

# display = Display(display_resolution=(1024, 768), display_diameter=16, display_distance=24)
# path = 'C:/Users/radzi/OneDrive/Desktop/II/Project/TestVideos/peat_small/13. Maroon 5 - Sugar (Official Music Video)_peat.avi'
# result, breaches = w3c_guideline.analyse_file(path, speedup=3, show_live_analysis=False, show_live_chart=False)
# print(result)
# print(breaches)
# result, breaches = w3c_guideline.analyse_file(path, speedup=3, show_live_analysis=False, show_live_chart=False)
# result, breaches = w3c_guideline.analyse_live(speedup=10, show_live_analysis=True, show_live_chart=True)
# print(result)
# video_censor(path, breaches, fallback_frames=6, frames_before=30)
# path = 'C:/Users/radzi/OneDrive/Desktop/II/Project/TestVideos/peat_small/13. Maroon 5 - Sugar (Official Music Video)_peat_censored.avi'
# result, breaches = w3c_guideline.analyse_file(path, speedup=3, show_live_analysis=False, show_live_chart=False)
# print(result)
# print(breaches)
#
# path = 'C:/Users/radzi/OneDrive/Desktop/II/Project/MediaOut/video_censored.avi'
# result, _ = w3c_guideline.analyse_file(path, display=display, speedup=3, show_live_analysis=False, show_live_chart=False)
# print(result)

# w3c_guideline.analyse_live(speedup=3, show_live_analysis=False, show_live_chart=False)
# from sklearn.metrics import accuracy_score
# import glob
#
# files = glob.glob("C:/Users/radzi/OneDrive/Desktop/II/Project/TestVideos/peat_small/*")
# print(files)
#
# all_accuracies = []
# all_results = []
# all_times = []
# for file in files:
#     result_three, breaches_three = w3c_guideline.analyse_file(file, speedup=3, show_live_analysis=False, show_live_chart=False)
#     accuracies = []
#     results = []
#     times = []
#     for i in [1, 1.5, 3, 6, 15, 30, 60, 150]:
#         start = time.time()
#         result, breaches = w3c_guideline.analyse_file(file, speedup=i, show_live_analysis=False, show_live_chart=False)
#         times.append(time.time()-start)
#         accuracies.append(accuracy_score(breaches_three, breaches))
#         results.append(result == result_three)
#     print(accuracies, results, times)
#     all_accuracies.append(accuracies)
#     all_results.append(results)
#     all_times.append(times)
# print(all_accuracies)
# print(all_results)
# print(all_times)
