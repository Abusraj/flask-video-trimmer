from datetime import date
from math import floor
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from moviepy.editor import *


app = Flask(__name__)
# download_path = os.path.join(os.path.abspath('./static')+'')
# app.config["SECRET_KEY"] = '666'
# path=os.path.join(download_path,"")


def pathdir(dir):
    return  os.path.join(os.path.abspath('./window/static'),dir)

# print(pathdir("h2"))

try:
    path = pathdir('')
    files = os.listdir(path)
    for i in files:
        os.remove(path+i)
except OSError as e:
    print(e)


@app.route('/')
def home():
    return render_template('base.html', utc_dt=date.today().strftime("%A %d. %B %Y"))


@app.route('/video', methods=['POST'])
def videorender():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        location = pathdir(filename)
        f.save(location)
        x = 0  # start trimming
        i = 49  # end trimming on 49 second
        n = 0  # number of videos trimmed
        # Start from 0 to the duration(the end of the video)
        dur = VideoFileClip(location).duration
        list = []
        while (i <= int(dur)):
            clip = VideoFileClip(location).subclip(x, i)
            x += 49  # go to the next 49 second
            i += 49  # end at the next 49 second
            clip.write_videofile(pathdir(str(n)+".mp4"))
            list.append(pathdir(str(n)+".mp4"))
            n += 1
        if (floor(x) != 49):
            clip = VideoFileClip(location).subclip(x, dur)
            clip.write_videofile(pathdir(str(n)+".mp4"))
            list.append(pathdir(str(n)+".mp4"))
    return render_template("video.html", utc_dt=date.today().strftime("%A %d. %B %Y"), videos=list)


app.run(debug=True)
