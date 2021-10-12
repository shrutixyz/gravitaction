const video = document.querySelector('#videostream');
const output = document.querySelector('#output');
const audio = document.querySelector('#audiostream');
const recordBtn = document.querySelector('#record-btn');
const stopBtn = document.querySelector('#stop-btn');
const submitBtn = document.querySelector('#submit-btn');
const transcriptInput = document.querySelector('.subtitle');

const minutesDiv = document.getElementById('minutes');
const secondsDiv = document.getElementById('seconds');

const resultTranscript = document.querySelector('#transcript-result');
const resultClock = document.querySelector('#clock-result');
const resultConfidence = document.querySelector('#confidence-result');

//initialise time
var timerVar;
var count = 0;
var moveCount = 0;
var before = 0;

//initialise speech recog
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;


const recognition = new SpeechRecognition();
recognition.interimResults = true;
recognition.lang = 'en-US';
// recognition.continuous = true;

let p = document.createElement('p');
let r;
transcriptInput.appendChild(p);

function startRender(input, output, model) {
    const ctx = output.getContext("2d");
    async function renderFrame() {
      requestAnimationFrame(renderFrame);
      const faces = await model.estimateFaces(input, false, false);
      ctx.clearRect(0, 0, output.width, output.height);
      faces.forEach(face => {
        face.scaledMesh.forEach(xy => {
            count++;
          ctx.beginPath();
          ctx.arc(xy[0], xy[1], 1, 0, 2 * Math.PI);
          ctx.fill();
          if(Math.abs(xy[0]-before)>20){
              moveCount++;
          }
          before = xy[0]
          console.log(xy[0])
        });
      });
    }
    renderFrame();
  }


function showResults(){
    console.log("move"+moveCount);
    console.log("count" + count);
    var raw = moveCount*165/count;
    // moveCount = 3*moveCount/5
    console.log("raw: "+raw);
    var final = 30;
    if(moveCount*165/count >90){
        final = (90-moveCount/count); 
    }
    else{
        final  = raw ;
    }
    if(final<30){
        final = 35;
    }
    return final
}

recognition.addEventListener('result', e => {
    p.textContent = "\n"
    const lol = Array.from(e.results)
        .map(result => result[0])
        .map(result => result.transcript)
        .join('\n');
    
    p.textContent =  lol ;
       
    

    if (e.results[0].isFinal) {

        transcriptInput.appendChild(p)
        transcriptInput.scrollTop = transcriptInput.scrollHeight;
        
    }
        
});

recognition.addEventListener('end', () => {
    if(video.classList.contains('play')){
        console.log('restart')
        recognition.start()
        transcriptInput.innerText += " ... "
    }
});

   

recordBtn.addEventListener('click', async (e) => {
    console.log('record btn clicked')
    
   
    window.navigator.mediaDevices.getUserMedia({ video: true, audio:true })
    .then(stream => {
        window.localStream = stream;
        video.srcObject = stream;
        video.onloadedmetadata = e => {
            video.play()
        }
        audio.srcObject = stream;

        video.classList.add('play');
       
        recognition.start();
        console.log('recognition');
    })
    .catch( () => {
        alert('You have to give browser the permission to run Webcam and mic ;( ');
    });

    //start facemesh
    const model = await facemesh.load({maxFaces : 1})
    startRender(video, output, model)


    //start timer
    timerVar = setInterval(countTimer, 1000);
    var totalSeconds = 0;
    function countTimer() {
            ++totalSeconds;
            var hour = Math.floor(totalSeconds /3600);
            var minute = Math.floor((totalSeconds - hour*3600)/60);
            var seconds = totalSeconds - (hour*3600 + minute*60);
            if(hour < 10)
                hour = "0"+hour;
            if(minute < 10)
                minute = "0"+minute;
            if(seconds < 10)
                seconds = "0"+seconds;

            minutesDiv.innerText = minute;
            secondsDiv.innerText = seconds;
            //    document.getElementById("timer").innerHTML = hour + ":" + minute + ":" + seconds;
    }


})


stopBtn.addEventListener('click', e => {
    console.log('pause')

    //stop timer
    clearInterval(timerVar)

    localStream.getVideoTracks()[0].stop();
    video.src = '';
    
    localStream.getAudioTracks()[0].stop();
    audio.src = '';

    video.classList.remove('play')
 })


submitBtn.addEventListener('click', e => {

    const confidence = showResults()
    resultTranscript.value = transcriptInput.textContent;

  

    m = parseInt(minutesDiv.textContent)
    s = parseInt(secondsDiv.textContent)
    time = m * 60 + s
    resultClock.value = time;

    resultConfidence.value = confidence;


    // console.log(resultConfidence.value)
})

