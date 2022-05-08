import os

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

import glob

from PhotosensitivitySafetyEngine.PhotosensitivitySafetyEngine.video_tools import video_convert

files = glob.glob("C:/Users/radzi/OneDrive/Desktop/II/Project/TestVideos/*")
for file in files:
    print(file)
    video_convert.convert_to_peat(file)
