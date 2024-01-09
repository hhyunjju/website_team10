

    // The width and height of the captured photo. We will set the
    // width to the value defined here, but the height will be
    // calculated based on the aspect ratio of the input stream.
  
    var width = 720;    // We will scale the photo width to this
    var height = 0;     // This will be computed based on the input stream
  
    // |streaming| indicates whether or not we're currently streaming
    // video from the camera. Obviously, we start at false.
  
    var streaming = false;
  
    // The various HTML elements we need to configure or control. These
    // will be set by the startup() function.
  
    var video = null;
    var canvas = null;
    var photo = null;
    var startbutton = null;
    var sendImg = null;
    var myTracks = null;
    var streamingStatus = false;
  
    function startup() {
      video = document.getElementById('video');
      canvas = document.getElementById('canvas');
      photo = document.getElementById('photo');
      startbutton = document.getElementById('startbutton');
      pausebutton = document.getElementById('pausebutton');
      stopbutton = document.getElementById('stopbutton');

      const constraints = {
        video: {
            frameRate: {
                ideal: 10, max: 15
            },
        }, 
        audio: false,
        };

        navigator.mediaDevices
        .getUserMedia(constraints)
        .then((mediaStream) => {
            video.srcObject = mediaStream;
            myTracks = video.srcObject.getTracks();
            
        })
        .catch((err) => {
            console.error(`${err.name}: ${err.message}`);
        });

        
  
        video.addEventListener('canplay', function(ev){
          if (!streaming) {
            height = video.videoHeight / (video.videoWidth/width);
          
            // Firefox currently has a bug where the height can't be read from
            // the video, so we will make assumptions if this happens.
          
            if (isNaN(height)) {
              height = width / (4/3);
            }
          
            video.setAttribute('width', width);
            video.setAttribute('height', height);
            canvas.setAttribute('width', width);
            canvas.setAttribute('height', height);
            streaming = true;
          }
        }, false);
    
        // startVideo();

        gameOneSet();

        clearphoto();
    }


    function to_service(){
      window.location.href = "http://localhost:8000/service/service";
    }

    function startVideo() {
      video.play();
      streamingStatus = true;
      // sendImg = setInterval(sendImage, 3000);
    }

    function stopVideo() {
      if(streamingStatus){
        video.srcObject.getTracks().forEach( (track) => {
          track.stop();
          });''
        streamingStatus = false;
        to_service();
      }
    }


  
    // Fill the photo with an indication that none has been
    // captured.
  
    function clearphoto() {
      var context = canvas.getContext('2d');
      context.fillStyle = "#AAA";
      context.fillRect(0, 0, canvas.width, canvas.height);
  
      var data = canvas.toDataURL('image/png');
      photo.setAttribute('src', data);
    }
    
    // Capture a photo by fetching the current contents of the video
    // and drawing it into a canvas, then converting that to a PNG
    // format data URL. By drawing it on an offscreen canvas and then
    // drawing that to the screen, we can change its size and/or apply
    // other changes before drawing it.

    let answer = [];

    function sendImage() {
      var context = canvas.getContext('2d');
      canvas.width = width;
      canvas.height = height;
      // console.log(width);
      // console.log(height);
      context.translate(video.width, 0);
      context.scale(-1, 1);
      context.drawImage(video, 0, 0, width, height);

      var picdata = canvas.toDataURL('image/png');
      photo.setAttribute('src', picdata);

      canvas.toBlob(blob => {
        const jpegBlob = new Blob([blob], { type: 'image/png' });
        const fileName = 'canvas_img_' + new Date().getMilliseconds() + '.png';
        // const formData = new FormData();
        // formData.append('camera-image', blob);
        var data = new FormData($('form')[0]);
        // var picdata = canvas.toDataURL('image/png');
        data.append("img_file", jpegBlob, fileName);
        console.log('form에 이미지 추가');

        

        $.ajax({
          type : "POST",
          url : "/service/send_image_game/", // 통신할 url을 지정
          // enctype : "multipart/form-data",
          processData : false,
          contentType : false,
          data: data,
          datatype: 'json',
          success: function (data) {
            // console.log(data);
            console.log('success');
            console.log('stretching : '+data['class_name']);
            // jQuery("#posture-status").html(Number(data['class_name'])); // #########
            if (jQuery("#posture-status").html()==data['class_name']) {
              // $('#stretchingStatus').html('O');
              answer.push(1);
            }
            else {
              // $('#stretchingStatus').html('X');
              answer.push(0);
            }
            console.log("현재 정답 : "+answer);
          },
          error: function(e){
            console.log('error');
          }
        });
      }, 'image/png');
      console.log(streaming);
    }

// ######################################################## Timer
    function TIMER(time, min, sec){
      PLAYTIME=setInterval(function(){
            time=time-1000; //1초씩 줄어듦
            min=time/(60*1000); //초를 분으로 나눠준다.
    
           if(sec>0){ //sec=60 에서 1씩 빼서 출력해준다.
                sec=sec-1;
                jQuery("#count").html(sec);
               
            }
            if(sec===0){
               // 0에서 -1을 하면 -59가 출력된다.
                // 그래서 0이 되면 바로 sec을 60으로 돌려주고 value에는 0을 출력하도록 해준다.
                sec=60;
                jQuery("#count").html('0');
            }    
            if($('#count').html()=='0'){
              jQuery("#count").html('시간 종료');
            } 
            
       
        },1000); //1초마다 
    }

    function myTimer(sen, time, m, s) {
      return new Promise(resolve => {
        jQuery("#count").html(s);
        jQuery("#subscription").html(sen);
        TIMER(time,m,s);
        setTimeout(() => {
          clearInterval(PLAYTIME);
          resolve();
      }, time);
      });
    }

    function myTimer2(sen, time, m, s) {
      return new Promise(resolve => {
        jQuery("#count").html(s);
        jQuery("#subscription").html(sen);
        TIMER(time,m,s);
        var sendimg = setInterval(sendImage, 1000);
        setTimeout(() => {
          clearInterval(sendimg);
          clearInterval(PLAYTIME);
          resolve();
      }, time);
      });
    }

    function mySendImage(){
      return new Promise(resolve => {
        sendImage();
        resolve();
      });
    }

    function myStartVideo(){
      return new Promise(resolve => {
        setTimeout(() => {
          startVideo();
          resolve();
      }, 700);
        // startVideo();
        // resolve();
      });
    }

    function myStopVideo(){
      return new Promise(resolve => {
        setTimeout(() => {
          stopVideo();
          resolve();
      }, 5000);
        // startVideo();
        // resolve();
      });
    }

    function tryAgain() {
      return new Promise(resolve => {
        var sentence = '맞을 때까지 나갈 수 없습니다.\n 다시 해 보세요';
        jQuery("#subscription").html(sentence);
        failSignal();
        resolve();
      });
    }

    var correct = true;

    function myAnswer() {
      return new Promise(resolve => {
        // try {
        //   console.log('answer 호출 : '+answer);
        //   console.log('*****************find 1 :'+answer.find(1));
        //   answer.find(1);
        //   $('#stretchingStatus').html('O');
        // } catch(error) {
        //   console.log(error);
        //   console.log('그럼 여기로 오나?');
        //   $('#stretchingStatus').html('X');
        // }
        console.log('최종 answer : '+answer);
        if(answer.indexOf(1)==-1){
          console.log('실패');
          $('#stretchingStatus').html('X');
          correct = false;
        } else if (answer.indexOf(1)>=0){
          correct = true;
          console.log('성공');
          $('#stretchingStatus').html('O');
        }
        resolve();
      });
    }

    function gameOneSet(){
      myTimer('5초 뒤에 스트레칭이 시작됩니다.', 5000, 0, 5)
        .then(() => {
          return myStartVideo();
        })
        .then(() => {
          return myTimer2('왼쪽의 동작을 10초 동안 따라해주세요.', 10000, 0, 10);
        })
        .then(() => {
          return myAnswer();
        })
        .then(() => {
          return myStopVideo();
        })
    }


    window.addEventListener('load', startup, false);

