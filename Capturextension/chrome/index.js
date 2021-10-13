(() => {
  const EXTENSION_ID = 'biedcckmiaepfaciienbodgiiklnpflb';

  const video = document.getElementById('screen-view');
  const getScreen = document.getElementById('get-screen');
  const stopScreen = document.getElementById('stop-screen');
  const request = { sources: ['window', 'screen', 'tab'] };
  let stream;
  getScreen.addEventListener('click', event => {
    chrome.runtime.sendMessage(EXTENSION_ID, request, response => {
      if (response && response.type === 'success') {
        navigator.mediaDevices.getUserMedia({
          video: {
            mandatory: {
              chromeMediaSource: 'desktop',
              chromeMediaSourceId: response.streamId,
            }
          }
        }).then(returnedStream => {
          stream = returnedStream;
          video.srcObject = stream;
          getScreen.style.display = "none";
          stopScreen.style.display = "inline";
        }).catch(err => {
          console.error('Could not get stream: ', err);
        });
      } else {
        console.error('Could not get stream');
      }
    });
  });
  stopScreen.addEventListener('click', event => {
    stream.getTracks().forEach(track => track.stop());
    video.src = '';
    stopScreen.style.display = "none";
    getScreen.style.display = "inline";
  });
})();
