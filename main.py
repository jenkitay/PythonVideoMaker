# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import os.path
from os import path
import moviepy.editor as mpy
from datetime import datetime
import csv
import gc
from pprint import pprint

color_print = {
    'white':    "\033[1;37m",
    'yellow':   "\033[1;33m",
    'green':    "\033[1;32m",
    'blue':     "\033[1;34m",
    'cyan':     "\033[1;36m",
    'red':      "\033[1;31m",
    'magenta':  "\033[1;35m",
    'black':      "\033[1;30m",
    'darkwhite':  "\033[0;37m",
    'darkyellow': "\033[0;33m",
    'darkgreen':  "\033[0;32m",
    'darkblue':   "\033[0;34m",
    'darkcyan':   "\033[0;36m",
    'darkred':    "\033[0;31m",
    'darkmagenta':"\033[0;35m",
    'darkblack':  "\033[0;30m",
    'off':        "\033[0;0m"
}

def list_fonts():
    clip = mpy.TextClip.list('font')
    for i in clip:
        print(i)


def list_colors():
    clip = mpy.TextClip.list('color')
    for i in clip:
        print(i)


def make_movie(file_name, vid_list, text_list, image):
    clips = []
    # f = 0
    # Generate an image clip
    logo_image = mpy.ImageClip(image).resize(width=275)

    for vid, txt in zip(vid_list, text_list):
        # load video without sound
        clip = mpy.VideoFileClip(vid, audio=False)
        cy = clip.h
        cx = clip.w
        # TODO: Uncomment Production variable
        # d = 2                   # for test only
        d = clip.duration     # for production
        # print("duration = {0}".format(d))
        # clipping of the video from start time to end time in seconds.
        clip = clip.subclip(0, d)

        # Reduce the audio volume (volume x 0.8)
        # clip = clip.volumex(0.8)

        # Generate a text clip
        txt_clip = mpy.TextClip(" " + txt + " ", fontsize=50, color='black')
        tx, ty = txt_clip.size    # width and height of clip
        if tx > cx - 100:
            txt_clip = mpy.TextClip(" " + txt + " ", fontsize=50, color='black',
                                    method='caption', size=(cx - 100, None), align='West')
            tx, ty = txt_clip.size    # width and height of clip
        # add background to text clip
        txt_bg = mpy.ColorClip((tx, ty), color=(255, 255, 255)).set_opacity(.75)
        txt_bg = txt_bg.set_position((cx - tx - 50, cy - ty - 50)).set_duration(d)
        txt_clip = txt_clip.set_position((cx - tx - 50, cy - ty - 50)).set_duration(d)

        # logo_clip.resize(width=400)  # height computed automatically.
        logo_clip = logo_image.set_position((50, 50)).set_duration(d)

        # Overlay the text clip on the first video clip
        video = mpy.CompositeVideoClip([clip, txt_bg, txt_clip, logo_clip])
        video = video.margin(5, color=(0, 0, 0)).margin(5, color=(234, 159, 168)).margin(5, color=(0, 0, 0))

        # if f:
        #     video = video.crossfadein(1.5)
        # f += 1
        clips.append(video)

        # clip.close()
        # txt_bg.close()
        # txt_clip.close()
        # logo_clip.close()

    # make video
    final_clip = mpy.concatenate_videoclips(clips)
    # TODO: Set fps to 24 instead of 12
    final_clip.write_videofile(file_name, fps=24, audio=False, preset='veryfast')
    # final_clip.close()

# my_clip.write_gif('test.gif', fps=12)


if __name__ == '__main__':
    data = []
    resource_directories = ["E:/Old_MEMC_Videos/Phase 1/Trimmed Videos/",
                            "E:/Old_MEMC_Videos/Phase 1/2 Trimmed Videos 2/",
                            "E:/Old_MEMC_Videos/Phase 1/3 Trimmed Videos 3/",
                            "E:/Old_MEMC_Videos/Phase 1/4 Trimmed Videos 4/",
                            "E:/Old_MEMC_Videos/Phase 1/5 Trimmed Videos 5/",
                            "E:/Old_MEMC_Videos/Phase 1/6 Trimmed Videos 6/",
                            "E:/MEMC_Videos/Trimmed/Trimmed Videos/",
                            "E:/MEMC_Videos/Trimmed/2 Trimmed Videos 2/",
                            "E:/MEMC_Videos/Trimmed/3 Trimmed Videos 3/",
                            "E:/MEMC_Videos/Trimmed/4 Trimmed Videos 4/",
                            "E:/MEMC_Videos/Trimmed/5 Trimmed Videos 5/",
                            "E:/MEMC_Videos/Trimmed/6 Trimmed Videos 6/",
                            "E:/MEMC_Videos/Trimmed/7 Trimmed Videos 7/",
                            "E:/MEMC_Videos/Trimmed/8 Trimmed Videos 8/",
                            "E:/MEMC_Videos/Trimmed/Trimmed Videos 9/",
                            "E:/MEMC_Videos/Trimmed/Trimmed Videos 10/",
                            "E:/MEMC_Videos/Trimmed/Trimmed Videos 11/",
                            "E:/MEMC_Videos/All Trimmed/"]
    destination_directory = "E:/MEMC_Videos/Finished/output21/"
    count_total = 0
    count_done = 0

    # Load Data from csv file into list data[]
    with open('resources/videos_data.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            resource_directory = ""
            found_files = 0
            input_filename = row["Input Video file name"]

            # Check for duplicate paths
            for p in resource_directories:
                if path.isfile(p + input_filename):
                    found_files += 1
                    # check for duplicate files
                    if found_files > 1:
                        f = ""
                        if row["Output Video file name"]:
                            f = row["Output Video file name"] + ".mp4"
                        else:
                            f = path.basename(data[-1][0])
                        print(10*"*"+f" Duplicate files Found for {f}! "+10*"*")
                        print(f"Duplicate Path 1: {resource_directory + input_filename}")
                        print(f"Duplicate Path 2: {p + input_filename}")
                    resource_directory = p

            # Append video to data[]
            if row["Output Video file name"]:
                data.append([destination_directory + row["Output Video file name"] + ".mp4",
                             [row["Video Clip Heading"].title()],
                             [resource_directory + row["Input Video file name"]]])
                count_total += 1
            # Append resource to last video in data[]
            elif row["Input Video file name"] or row["Video Clip Heading"]:
                d = data[-1]
                d[-1].append(resource_directory + row["Input Video file name"])
                d[-2].append(row["Video Clip Heading"].title())
            else:
                continue


    # pprint(data)

    outputfilename = ""
    videos = []   # list of video paths
    titles = []   # list of titles
    logo = "resources/horizontal_MEMC_100opacity.png"


    for d in data:
        found_all = True
        outputfilename = d[0]
        titles = d[1]
        videos = d[2]
        for v in videos:
            if not path.isfile(v):
                print(f">>> File {v} not found! <<<")
                found_all = False
        outdir = path.dirname(outputfilename)
        if not path.isdir(outdir):
            print(f"!!! Directory {outdir} does not exist!")
            found_all = False
        if found_all:
            print(color_print['darkblue'] + f"*** Found all files needed to make {outputfilename}! ***" + color_print['off'])
            start = datetime.now()
            make_movie(outputfilename, videos, titles, logo)
            n = gc.collect()
            print("Garbage collected by GC:", n)
            # print("Uncollectable garbage:", gc.garbage)
            end = datetime.now()
            count_done += 1
            if path.exists(outputfilename):
                print(color_print['darkgreen'] + f"Success! {color_print['yellow'] + str(count_done)} / " +
                      f"{str(count_total) + color_print['darkgreen']} videos done!" + color_print['off'])
                print(f"Made video {outputfilename} in {end - start} (hh:mm:ss.ms)")
            else:
                print(color_print['red'] + f"###### There was a problem making {outputfilename} ######" + color_print['off'])
        else:
            print(color_print['red'] + f"###### Make Movie {outputfilename} Aborted! ######" + color_print['off'])

    # pprint(data)

