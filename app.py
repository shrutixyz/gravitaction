from flask import Flask, render_template, request
import cv2
import moviepy.editor as mp
import numpy as np
from PIL import Image
from ISR.models import RDN, RRDN
import os


UPLOAD_FOLDER = 'uploadFile'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
model = RDN(weights='noise-cancel')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enhance')
def enhance():
    return render_template('enhance/enhance.html')

@app.route('/analyse')
def analyse():
    return render_template('analyse/analyse.html')


@app.route('/analyse_results')
def analyse_results():
    return render_template('analyse/analyse_results.html')

@app.route('/enhance_results')
def enhance_results():
    return render_template('enhance/enhance_results.html')



@app.route("/extract_frames", methods=['POST'])
def extract_frames():
    video = request.files['file1']
    video.save('video/video.mp4')
    print("vid saved")
    my_clip = mp.VideoFileClip(r"video/video.mp4")
    my_clip.audio.write_audiofile(r"audio/audio.mp3")
    print("audio extracted")
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
        img_isr = Image.open('frames/'+str(i)+'.png')
        print("open frame for scaling")
        # img_isr.resize(size=(img_isr.size[0]*4, img_isr.size[1]*4), resample=Image.BICUBIC)
        print("no resize")
        sr_img = model.predict(np.array(img_isr))
        print("resize done")
        image_enhanced = Image.fromarray(sr_img)
        image_enhanced.save('frames/enhanced'+str(i)+'.png', 'PNG')
        print("new image saved")
        print("i is" + str(i))
        i+=1
    cap.release()
    cv2.destroyAllWindows()
    print(i)
    print("made frames")

    return str(i)


if __name__ == "__main__":
    app.run(debug=True)



