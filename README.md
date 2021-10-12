# ECSTATIC
### analyse speeches and enhance video qualities, with so many built in features!

<br><br>

# Run locally
- Make sure you've python installed.
- clone the repository ```git clone https://github.com/shrutigupta5555/gravitaction```
- Go into the root directory and run ```pip install requirements.txt```
- Run ```python app.py```

# What is Ecstatic all about?

A user can primarily do two things on ecstatic <br>
- Enhance Videos <br>
It lets user upload their video, probably a low quality one so that ecstatic can enhance them, and then the work starts to happen behind the scene. The audio is extracted first, and then the video is broken down frame-by-frame. And then through the help of python libraries like MoviePy and OpenCV, each and every frame is enhanced using filters such as median blur, gaussian blur. Then at last, the frames are joined again and the audio is added as well and the output file is ready to be downloaded by the user!
Once the final video is ready, the script performs a cleanup and deleted all the files taken from user!
- Analyze Speeches/Presentations <br>
In this section, user just need to start recording [they should give mic and camera access to the browser] and then they can continue the speech or presentation like a rehearsal. Ecstatic would then perform various things, including-<br>
   - Speech to text, which in turn performs grammar check and tells the score.
   - Vocabulary index, which analyses how good was users vocabulary and usage of words.
   - Confidence, if the user seemed confident enough while delivering their content.
   - Pace of speech, by dividing the total words spoken by total time taken.

# How does it work?
- As the basic framework for our app, we used python's flask library.
- The webpages are made and designed using HTML5 and CSS3
- To enhance videos, we used OpenCV that breaks it down into frames, and applies filter. To extract the audio, we used MoviePy library and the same was used to join frames as well as to add back the audio.
- To analyse speeches, we used IBM's speech recognition to get the transcript, facemesh to check face's position to calculate confidence score, grammar checker to check grammatical errors.
- The whole flask application is deployed on graviton based EC2 instances.

# Images/Testimonials

## Before after of a random frame from test-video while performing enhancement <br><br>
Before <br>
![image](https://user-images.githubusercontent.com/69726390/136959769-e87b5dd7-5085-4925-be36-b116c415b7ec.png)
<br><br>After <br>
![image](https://user-images.githubusercontent.com/69726390/136959603-c6e7d4ea-55f9-4e0e-9be0-db2f9a0c4986.png)

## Results after performing anaylysis of speech/presentation

![image](https://user-images.githubusercontent.com/69726390/136960483-bed9b0f8-6076-4b13-a21f-7fa65cccc6b6.png) <br>
![image](https://user-images.githubusercontent.com/69726390/136960513-d87814d9-bc39-4c7d-9c97-7e9e83816d12.png)



