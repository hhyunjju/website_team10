  //----------1분마다 알람 울리기-------------
// 페이지 로드 시 알림 권한 요청
window.onload = function() {
    askNotificationPermission();
};

let globalNotification = null;

// 알림 생성 함수
function makeNoti() {
    // 이미 알림이 활성화되어 있다면 새 알림을 생성하지 않음
    if (globalNotification) {
        return;
    }

    // 권한이 허용된 경우에만 알림 생성
    // 회원가입시 이름을 받으면 => 알림에 이름을 넣을 수 있음
    // 랜덤으로 문구 나가도록 수정 or 라벨 반영해서 문구 수정
    if (Notification.permission === "granted") {
        globalNotification = new Notification("자세 경고", {
            body: "자세가 올바르지 않습니다.\n건강을 위해 바른 자세를 취해주세요",
            requireInteraction: true, // 사용자 상호작용이 필요
        });

        // 알림 클릭 이벤트 처리
        globalNotification.addEventListener("click", () => {
            window.open('https://www.naver.com/');
            globalNotification.close();
            globalNotification = null; // 전역 알림 객체 초기화
        });
    } else if (Notification.permission !== "denied") {
        // 권한 요청
        Notification.requestPermission().then(permission => {
            if (permission === "granted") {
                makeNoti();
            }
        });
    }
}

// 알림 닫기 함수
function closeNotification() {
    if (globalNotification) {
        globalNotification.close();
        globalNotification = null; // 전역 알림 객체 초기화
    }
}

// 권한 요청 함수
function askNotificationPermission() {
    if (!("permission" in Notification)) {
        Notification.requestPermission().then(permission => {
            Notification.permission = permission;
        });
    }
}

// 브라우저가 알림을 지원하는지 확인
if (!("Notification" in window)) {
    console.log("이 브라우저는 알림을 지원하지 않습니다.");
} else {
    askNotificationPermission();
}

// 전역 스코프에서 함수 사용 가능하도록 설정
window.makeNoti = makeNoti;
window.closeNotification = closeNotification;