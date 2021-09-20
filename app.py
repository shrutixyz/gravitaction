from flask import Flask, render_template
import cv2
import extract as ext


# port = int(os.environ.get('PORT', 5000))

app = Flask(__name__)
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

@app.route("/extract_frames/", methods=['POST'])
def extract_frames():
    print("started")
    cap= cv2.VideoCapture('E:/test.mp4') # add file path here dynamically
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
    return str(i)


if __name__ == "__main__":
    app.run(debug=True)



