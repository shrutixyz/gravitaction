from flask import Flask, render_template, request
import cv2
import extract as ext
import glob


# port = int(os.environ.get('PORT', 5000))
UPLOAD_FOLDER = 'uploadFile'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config["DEBUG"] = True


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enhance')
def enhance():
    return render_template('enhance.html')

@app.route('/analyse')
def analyse():
    return render_template('analyse.html')

@app.route("/extract_frames", methods=['POST'])
def extract_frames():
    video = request.files['file1']
    video.save('video/video.mp4')
    print("started")
    cap= cv2.VideoCapture('video/video.mp4') # add file path here dynamically
    cap.set(cv2.CAP_PROP_FPS, 60) # this isnt working rn idk why, taking 30fps only
    i=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite('frames/'+str(i)+'.png',frame)
        i+=1
    cap.release()
    cv2.destroyAllWindows()
    print(i)
    print("made frames")
    # gotta add photo enhance function and put into array and join
    # img_array = []
    # for filename in glob.glob('frames/*.jpg'):
    #     img = cv2.imread(filename)
    #     height, width, layers = img.shape
    #     size = (width,height)
    #     img_array.append(img)
 
    
    # out = cv2.VideoWriter('final/final.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
    # for i in range(len(img_array)):
    #     out.write(img_array[i])
    # out.release()
    # print("ban gayi firse video") #can be find in final.mp4, should be given to users to download
    return str(i)


if __name__ == "__main__":
    app.run(debug=True)



