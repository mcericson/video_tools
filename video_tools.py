import os
import cv2
import moviepy.video.io.ImageSequenceClip
from moviepy.editor import VideoFileClip, clips_array, concatenate_videoclips, vfx
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip



"""This is small library of tools built on the moviepy and opencv.  
    1.Install openCV and moviepy
    2. Move videos to same directory as video_tools.py
    3. Create a new python file with and import video_tools.py
    4. Call the appropriate functions and run. :)"""

def numbered_name(number, name, padding):
    num = str(number) 
    num_pad = num.zfill(padding)
    file_name = num_pad + "_" + name
    return file_name


def image_resize(file_path, width, height, file_name):
    img = cv2.imread(file_path)
    w = int(width)
    h = int(height)
    new_dim = (w, h)
    new_image = cv2.resize(img, new_dim, interpolation = cv2.INTER_AREA )
    image_file = cv2.imwrite(file_name, new_image)
    return file_name
    

def make_movie(fps, width, height, file_name):
    """Makes a movie from a set of images.  Forces images to same size by setting widht and height parameters. """
    
    all_files = os.listdir()
    all_images = []
    
    for i in all_files:
        if i.endswith(".png"):
            all_images.append(i)
    count = 0
    resized_images = []
    for j in all_images:
        count += 1
        file_name_b = numbered_name(count, 'temp.png', 5)
        re_image = image_resize(j, width, height, file_name_b)
        resized_images.append(re_image)
           
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(resized_images, fps=fps)
    file_path = str(file_name) + ".mp4"
    clip.write_videofile(file_path)
    
    for m in resized_images:
        os.remove(m)

def resize_video(file_path, new_name, new_size):
    """resize a video video by specifying a new height in pixels"""
    clip = VideoFileClip(file_path)
    clip_resized = clip.resize(height=new_size)
    clip_resized.write_videofile(new_name + ".mp4")

def video_speed(video, speed_factor, new_file_name):
    """Place in folder. Provide start file, steep and destination file name:
    example:

    video_speed("guts.mp4", 4, "fast_guts.mp4")

    """
    clip = VideoFileClip(video)
    final_clip = clip.fx(vfx.speedx, speed_factor)
    final_clip.write_videofile(new_file_name)

def tile_video_linear(file_name):

    '''Tiles video clips in sequence. Place in folder.  Provide destination file name and run videos must be identical in format.
    example:

    tile_video_linear("guts.mp4")
    '''
    all_files = os.listdir()
    all_clips = []

    for i in all_files:
        if i.endswith(".mp4"):
            clip = VideoFileClip(i)
            all_clips.append(clip)

    final_clip = concatenate_videoclips(all_clips)

    final_clip.write_videofile(file_name)


def movie_clipper(startTimeM,starTimeS, endTimeM,endTimeS,sourceFile,targetFile):

    """clips a portion of a video into a new video
    ex:
    movie_clipper(0,30,0,50,"my_movie.mp4", "my_movie_trimmed.mp4")"""
    startTime = (startTimeM*60) + starTimeS
    endTime = (endTimeM*60) + endTimeS
    ffmpeg_extract_subclip(sourceFile, startTime ,endTime, targetname = targetFile)