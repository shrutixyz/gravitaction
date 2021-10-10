const video = document.querySelector('#videostream');
const audio = document.querySelector('#audiostream');
const recordBtn = document.querySelector('#record-btn');
const stopBtn = document.querySelector('#stop-btn');
const submitBtn = document.querySelector('#submit-btn');
const transcriptInput = document.querySelector('.subtitle');

const resultTranscript = document.querySelector('#transcript-result');
  
//initialise speech recog
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;


const recognition = new SpeechRecognition();
recognition.interimResults = true;
recognition.lang = 'en-US';
// recognition.continuous = true;

let p = document.createElement('p');
let r;
transcriptInput.appendChild(p);


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
        transcriptInput.innerText += "..."
    }
});

   

recordBtn.addEventListener('click', e => {
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

})


stopBtn.addEventListener('click', e => {
    console.log('pause')

    localStream.getVideoTracks()[0].stop();
    video.src = '';
    
    localStream.getAudioTracks()[0].stop();
    audio.src = '';

    video.classList.remove('play')
 })


submitBtn.addEventListener('click', e => {
    resultTranscript.value = transcriptInput.textContent;
    console.log(resultTranscript.value)
})