askNotificationPermission();

function makeNoti() {
  // 사용자 응답에 따라 단추를 보이거나 숨기도록 설정
  if (Notification.permission === "denied" || Notification.permission === "default") {
    alert("알림이 차단된 상태입니다. 알림 권한을 허용해주세요.");
  } else {

    let notification = new Notification("test", { // "test" => 제목
      body: "1시간이 지났습니다.", // 메세지
      icon: `/lib/img/novalogo_copy.png`, // 아이콘
    });

    //알림 클릭 시 이벤트
    notification.addEventListener("click", () => {
        window.location.href = "http://localhost:8000/service/game";
        notification.close();
    });

  }
}

function askNotificationPermission() {
  console.log("권한 묻기");
  // 권한을 실제로 요구하는 함수
  function handlePermission(permission) {
    // 사용자의 응답에 관계 없이 크롬이 정보를 저장할 수 있도록 함
    if (!("permission" in Notification)) {
      Notification.permission = permission;
    }
  }

  // 브라우저가 알림을 지원하는지 확인
  if (!("Notification" in window)) {
    console.log("이 브라우저는 알림을 지원하지 않습니다.");
  } else {
    if (checkNotificationPromise()) {
      Notification.requestPermission().then((permission) => {
        handlePermission(permission);
      });
    } else {
      Notification.requestPermission(function (permission) {
        handlePermission(permission);
      });
    }
  }
}

function checkNotificationPromise() {
  try {
    Notification.requestPermission().then();
  } catch (e) {
    return false;
  }

  return true;
}


// function notifyMe() {
//     if (!("Notification" in window)) {
//       // Check if the browser supports notifications
//       alert("This browser does not support desktop notification");
//     } else if (Notification.permission === "granted") {
//       // Check whether notification permissions have already been granted;
//       // if so, create a notification
//       const notification = new Notification("Hi there!");
//       // …
//     } else if (Notification.permission !== "denied") {
//       // We need to ask the user for permission
//       Notification.requestPermission().then((permission) => {
//         // If the user accepts, let's create a notification
//         if (permission === "granted") {
//           const notification = new Notification("Hi there!");
//           // …
//         }
//       });
//     }
  
//     // At last, if the user has denied notifications, and you
//     // want to be respectful there is no need to bother them anymore.
//   }

// #################################################################################################


// const Timer=document.getElementById('timer'); //스코어 기록창-분
let time= 5000;
let min=0;
let sec=5;


// Timer.value=min+":"+'00'; 
// jQuery("#timer").html(min+":"+'00');
jQuery("#timer").html('5');

function TIMER(){
    PlAYTIME=setInterval(function(){
        time=time-1000; //1초씩 줄어듦
        min=time/(60*1000); //초를 분으로 나눠준다.

       if(sec>0){ //sec=60 에서 1씩 빼서 출력해준다.
            sec=sec-1;
            Timer.value=Math.floor(min)+':'+sec; //실수로 계산되기 때문에 소숫점 아래를 버리고 출력해준다.
            jQuery("#timer").html(sec);
           
        }
        if(sec===0){
         	// 0에서 -1을 하면 -59가 출력된다.
            // 그래서 0이 되면 바로 sec을 60으로 돌려주고 value에는 0을 출력하도록 해준다.
            sec=60;
            Timer.value=Math.floor(min)+':'+'00';
            jQuery("#timer").html('0');
        }    
        if(Timer.value=='0:00'){
          Timer.value='시간 종료';
          return;
        } 
        
   
    },1000); //1초마다 
}


TIMER();
setTimeout(function(){
    clearInterval(PlAYTIME);
},5000);//5초가 되면 Timer 삭제