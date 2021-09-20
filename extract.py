import cv2

def extract_all():
    print("started")
    cap= cv2.VideoCapture('E:/test.mp4') # add file path here dynamically
    cap.set(cv2.CAP_PROP_FPS, 60)
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