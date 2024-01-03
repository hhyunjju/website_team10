import cv2
import mediapipe as mp
import joblib
import numpy as np
import pandas as pd
import time
from preprocessing import calculate_angle, calculate_distance, landmark_description

# MediaPipe holistic 모델 초기화
mp_holistic = mp.solutions.holistic

# 저장된 RandomForest 모델 로드
model = joblib.load('pose_classification_model.pkl')

# 웹캠 설정
cap = cv2.VideoCapture(0)

# 시간 측정을 위한 초기 시간 설정
prev_time = 0
interval = 0.3  # 0.3초 간격

# 자세 정보를 저장하는 변수 초기화
display_text = "Waiting..."

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue
        
        # 현재 시간
        current_time = time.time()

        # 이미지 처리
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)

        # 가시성 확인
        visibility = [landmark.visibility for landmark in results.pose_landmarks.landmark] if results.pose_landmarks else []
        avg_visibility = np.mean(visibility) if visibility else 0

        # 0.3초 간격으로 데이터 처리 및 가시성에 따른 조건부 실행
        if (current_time - prev_time) > interval:
            if avg_visibility > 0.1:  # 사람이 화면에 있을 경우
                pose_landmarks = results.pose_landmarks.landmark
                row = []
                for landmark in pose_landmarks:
                    row.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
                
                # 거리 및 각도 계산
                for i in range(len(pose_landmarks)):
                    for j in range(i+1, len(pose_landmarks)):
                        distance = calculate_distance([pose_landmarks[i].x, pose_landmarks[i].y, pose_landmarks[i].z],
                                                      [pose_landmarks[j].x, pose_landmarks[j].y, pose_landmarks[j].z])
                        row.append(distance)
                        if i < len(pose_landmarks) - 2 and j < len(pose_landmarks) - 1:
                            for k in range(j+1, len(pose_landmarks)):
                                angle = calculate_angle([pose_landmarks[i].x, pose_landmarks[i].y, pose_landmarks[i].z],
                                                        [pose_landmarks[j].x, pose_landmarks[j].y, pose_landmarks[j].z],
                                                        [pose_landmarks[k].x, pose_landmarks[k].y, pose_landmarks[k].z])
                                row.append(angle)
                
                # DataFrame으로 변환하고, 특성 이름을 지정
                csv_columns = ['file_name', 'label'] + [f'{name}_{dim}' for name in landmark_description for dim in ['x', 'y', 'z', 'visibility']]
                csv_columns += [f'distance_between_{landmark_description[i]}_and_{landmark_description[j]}' for i in range(len(landmark_description)) for j in range(i+1, len(landmark_description))]
                csv_columns += [f'angle_between_{landmark_description[i]}_{landmark_description[j]}_{landmark_description[k]}' for i in range(len(landmark_description)) for j in range(i+1, len(landmark_description)) for k in range(j+1, len(landmark_description))]
                row_df = pd.DataFrame([row], columns=csv_columns[2:])  # 컬럼명 적용

                # RandomForest 모델을 사용하여 자세 예측
                prediction = model.predict(row_df)
                class_name = prediction[0]

                # 자세 정보 업데이트
                display_text = f'Pose: {class_name}'

                # 다음 데이터 처리 시간 업데이트
                prev_time = current_time
            else:
                # 가시성이 낮을 때는 대기 메시지 표시
                display_text = "Waiting..."  

        # 화면에 자세 정보 표시 (깜빡임 방지)
        cv2.putText(frame, display_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # 결과 화면 표시
        cv2.imshow('Pose Classification', frame)
        
        # ESC 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == 27:
            break 
        
cap.release()
cv2.destroyAllWindows()
