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

address_in = "C:/Users/radzi/OneDrive/Desktop/II/Project/TestVideos/Resolutions/Video1.avi"
for j in range(8):
    res = (int(1920/2*(j+1)), int(1080/2*(j+1)))
    print(res)
    address_out = os.path.splitext(address_in)[0]+"_"+str(j+1)+'K.avi'
    writer = cv2.VideoWriter(address_out, 0, 30, res)
    capture = cv2.VideoCapture(address_in)
    for i in range(900):
        check, frame = capture.read()
        if not check:
            break
        frame2 = cv2.resize(frame, res)
        writer.write(frame2)
    writer.release()