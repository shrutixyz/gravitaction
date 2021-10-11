from flask import Flask, render_template, request
import cv2
import moviepy.editor as mp
import numpy as np
from PIL import Image
# from ISR.models import RDN, RRDN
from flask import send_file
import os
import glob
from moviepy.editor import *
from PIL import ImageEnhance

percent = 10
UPLOAD_FOLDER = 'uploadFile'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# model = RDN(weights='noise-cancel')
message = "Enhancing your awesome video..."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select')
def select():
    return render_template('select.html')

@app.route('/test')
def test():
    return render_template('test2.html')

@app.route('/enhance')

def enhance():
    return render_template('enhance/enhance.html', message=message, percent = str(percent) + "%")

@app.route('/analyse', methods = ['GET', 'POST'])
def analyse():
    form = ""
    if request.method == 'POST':
        form = request.form
        transcriptResult = request.form.getlist('ans')
        clockResult = request.form.getlist('time')
        print(transcriptResult, clockResult ,"here")
        print(form, "made a req")
    return render_template('analyse/analyse.html', form = form)


@app.route('/analyse_results')
def analyse_results():
    freq = [('singing', 15), ('eloquent', 7), ("party", 5), ("samosa", 4), ("jalebi", 2)]
    first = str(freq[0][1]*90/freq[0][1])+ "%"
    second = str(freq[1][1]*90/freq[0][1])+ "%"
    third = str(freq[2][1]*90/freq[0][1])+ "%"
    fourth = str(freq[3][1]*90/freq[0][1])+ "%"
    fifth = str(freq[4][1]*90/freq[0][1]) + "%"
    frequency = [first, second, third, fourth, fifth]
    names = [str(freq[0][0]), str(freq[1][0]), str(freq[2][0]), str(freq[3][0]), str(freq[4][0])]
    return render_template('analyse/analyse_results.html', names = names, frequency = frequency)

@app.route('/enhance_results')
def enhance_results():
    return render_template('enhance/enhance_results.html')


@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "final_vid.mp4"
    return send_file(path, as_attachment=True)




@app.route("/extract_frames", methods=['POST'])
def extract_frames():
    video = request.files['file1']
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
    # cap.set(cv2.CAP_PROP_FPS, 60) # this isnt working rn idk why, taking 30fps only
    i=0

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite('frames/'+str(i)+'.png',frame)
        print("Frame saved")
        # img_isr = cv2.imread('frames/'+str(i)+'.png')
        img_isr =  Image.open('frames/'+str(i)+'.png')
        print("Frame opened for scaling")
        # img_isr.resize(size=(img_isr.size[0]*4, img_isr.size[1]*4), resample=Image.BICUBIC)
        # print("beginning averaging")
        color = ImageEnhance.Color(img_isr)
        image_colored = color.enhance(1.5)
        # median = cv2.GaussianBlur(img_isr,(1,1),cv2.BORDER_DEFAULT)
        print("Filter applied")
        image_colored.save('frames/enhanced/'+str(i)+'.png')
        # Image.fromarray(median).save('frames/enhanced/'+str(i)+'.png')
        print("new image saved")
        print("The frame number is" + str(i))
        i+=1
    cap.release()
    cv2.destroyAllWindows()
    print(i)
    print("made frames")
    percent = 70
    # os.system("ffmpeg -r 30 -i frames/enhanced/img%01d.png -vcodec mpeg4 -y final_vid.mp4")
    print("Joining the frames started")
    img_array = []
    k = 0
    for j in glob.glob('frames/enhanced/*.png'):
        img = cv2.imread("frames/enhanced/"+str(k)+".png")
        k=k+1
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    print("Images appended")
    out = cv2.VideoWriter('final_vid.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
    print("Video released")
    percent = 80
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    print("final video processed")
    print("adding audio")
    clip = VideoFileClip("final_vid.avi")
    audioclip = AudioFileClip("audio/audio.mp3")
    print("finalizing audio")
    videoclip = clip.set_audio(audioclip)
    percent = 90
    videoclip.write_videofile("final_vid.mp4", fps=30, threads=1, codec="libx264")
    print("FINAL VIDEO PROCESSING DONE")
    video_size = os.stat('final_vid.mp4').st_size
    img_before = cv2.imread("frames/5.png")
    print("Saving one random frame")
    img_after = cv2.imread("frames/enhanced/5.png")
    # img_before.save("static/5.png")
    cv2.imwrite("static/5.png", img_before)
    # print("saving 5th frame cont")
    percent = 100
    cv2.imwrite("static/5enh.png", img_after)
    # img_after.save("")
    files = glob.glob('frames/*.png')
    for f in files:
        os.remove(f)
    print("Clearing memory")
    files = glob.glob('frames/enhanced/*.png')
    for f in files:
        os.remove(f)    
    print("removed enhanced frames")
    os.remove("final_vid.avi")
    # os.remove("audio/audio.mp3")
    return render_template("enhance/enhance_results.html", video_size = round(video_size/1048576, 2))


if __name__ == "__main__":
    app.run(debug=True)




# import cv2
# import numpy as np
# from PIL import Image 
# from PIL import ImageEnhance

# img_isr = cv2.imread('test2.png')
# print("Frame opened for scaling")
# img = Image.open('test2.png')
# # median = cv2.GaussianBlur(img_isr,-1, (9,9),cv2.BORDER_DEFAULT)
# # filterbaamzi = cv2.filter2D(src=image, ddepth=-1, (3,3))
# # box = cv2.boxFilter(img_isr, -1, (10, 10), normalize=True)
# bright = ImageEnhance.Brightness(img)
# image_brightened = bright.enhance(1.5)
# color = ImageEnhance.Color(img)
# image_colored = color.enhance(1.5)
# contrast = ImageEnhance.Contrast(img)
# image_contrasted = contrast.enhance(1.5)
# sharp = ImageEnhance.Sharpness(img)
# image_sharped = sharp.enhance(1.5)
# box = cv2.bilateralFilter(img_isr, 5, 10, 10) 
# image_brightened.save('bright.png')
# image_colored.save("colored.png")
# image_contrasted.save("constrast.png")
# image_sharped.save("sharp.png")
# print("Filter applied")
# # Image.fromarray(median).save('gaussian.png')
# Image.fromarray(box).save('box.png')
