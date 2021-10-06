const video = document.querySelector('#videostream');
const audio = document.querySelector('#audiostream');
const recordBtn = document.querySelector('#record-btn');
const stopBtn = document.querySelector('#stop-btn')
  
// video.srcObject = null;


   


recordBtn.addEventListener('click', e => {
    console.log('clicked')
    
    // video.play()
   
        // console.log(video)
        window.navigator.mediaDevices.getUserMedia({ video: true, audio:true })
        .then(stream => {
          window.localStream = stream;
          video.srcObject = stream;
          video.onloadedmetadata = e => {
              video.play()
          }
          audio.srcObject = stream;
        })
        .catch( () => {
            alert('You have to give browser the permission to run Webcam and mic ;( ');
        });
    
})


stopBtn.addEventListener('click', e => {
    // console.log('pause')
    localStream.getVideoTracks()[0].stop();
    video.src = '';
    
    localStream.getAudioTracks()[0].stop();
    audio.src = '';
})