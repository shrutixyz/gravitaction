from flask import Flask, render_template, request
import cv2
import moviepy.editor as mp
import numpy as np
from PIL import Image
from ISR.models import RDN, RRDN
from flask import send_file
import os
import glob
from moviepy.editor import *

percent = 10
UPLOAD_FOLDER = 'uploadFile'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
model = RDN(weights='noise-cancel')
message = "Enhancing your awesome video..."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enhance')

def enhance():
    return render_template('enhance/enhance.html', message=message, percent = str(percent) + "%")

@app.route('/analyse')
def analyse():
    return render_template('analyse/analyse.html')


@app.route('/analyse_results')
def analyse_results():
    return render_template('analyse/analyse_results.html')

@app.route('/enhance_results')
def enhance_results():
    return render_template('enhance/enhance_results.html')

@app.route('/test')
def test():
    return render_template('enhance/test.html')

@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "final_vid.mp4"
    return send_file(path, as_attachment=True)

@app.route('/progress')
def progress():
    return render_template('enhance/progress.html')

@app.route("/extract_frames", methods=['POST'])
def extract_frames():
    video = request.files['file1']
    message = "uploading to server... [1/8]"
    video.save('video/video.mp4')
    print("vid saved")
    global percent
    percent = 10
    my_clip = mp.VideoFileClip(r"video/video.mp4")
    my_clip.audio.write_audiofile(r"audio/audio.mp3")
    print("audio extracted")
    percent = 30
    print("started")
    cap= cv2.VideoCapture('video/video.mp4') # add file path here dynamically
    cap.set(cv2.CAP_PROP_FPS, 60) # this isnt working rn idk why, taking 30fps only
    i=0

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite('frames/'+str(i)+'.png',frame)
        print("save frame")
        img_isr = cv2.imread('frames/'+str(i)+'.png')
        print("open frame for scaling")
        # img_isr.resize(size=(img_isr.size[0]*4, img_isr.size[1]*4), resample=Image.BICUBIC)
        print("beginning averaging")
        median = cv2.medianBlur(img_isr,5)
        print("avg done")
        Image.fromarray(median).save('frames/enhanced/'+str(i)+'.png')
        # median.cv2.imwrite('frames/enhanced/'+str(i))
        # sr_img = model.predict(np.array(img_isr))
        # print("resize done")
        # image_enhanced = Image.fromarray(sr_img)
        # image_enhanced.save('frames/enhanced'+str(i)+'.png', 'PNG')
        print("new image saved")
        print("i is" + str(i))
        i+=1
    cap.release()
    cv2.destroyAllWindows()
    print(i)
    print("made frames")
    percent = 70
    # os.system("ffmpeg -r 30 -i frames/enhanced/img%01d.png -vcodec mpeg4 -y final_vid.mp4")
    print("starting join baamzi")
    img_array = []
    k = 0
    for j in glob.glob('frames/enhanced/*.png'):
        img = cv2.imread("frames/enhanced/"+str(k)+".png")
        k=k+1
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    print("appended")
    out = cv2.VideoWriter('final_vid.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
    print("released")
    percent = 80
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    print("final vid done")
    print("adding audio")
    clip = VideoFileClip("final_vid.avi")
    audioclip = AudioFileClip("audio/audio.mp3")
    print("finalizing audio")
    videoclip = clip.set_audio(audioclip)
    percent = 90
    videoclip.write_videofile("final_vid.mp4", fps=30, threads=1, codec="libx264")
    print("doneeeeeeeeee")
    video_size = os.stat('final_vid.mp4').st_size
    img_before = Image.open("frames/5.png")
    print("saving 5th frame")
    img_after = Image.open("frames/enhanced/5.png")
    img_before.save("static/5.png")
    print("saving 5th frame cont")
    percent = 100
    img_after.save("static/5enh.png")
    files = glob.glob('/frames/*.png')
    for f in files:
        os.remove(f)
    print("removed earlier frames")
    files = glob.glob('/frames/enhanced*.png')
    for f in files:
        os.remove(f)    
    print("removed enhanced frames")
    os.remove("final_vid.avi")
    return render_template("enhance/enhance_results.html", video_size = round(video_size/1048576, 2))


if __name__ == "__main__":
    app.run(debug=True)



