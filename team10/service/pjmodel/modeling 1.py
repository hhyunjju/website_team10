from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

# CSV 파일에서 데이터를 로드
data = pd.read_csv("C:/Users/user/Desktop/project/BigProject/data/output.csv")  # 올바른 파일 경로로 변경

# 특성(X)과 라벨(y)로 데이터 분리
X = data.drop(columns=['file_name', 'label'])  # 'file_name'과 'label' 컬럼 제거
y = data['label']  # 'label' 컬럼을 라벨로 사용

# 데이터를 학습 세트와 테스트 세트로 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Random Forest 모델 생성 및 학습
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 모델 저장
joblib.dump(model, 'pose_classification_model.pkl')

# 특성 중요도 출력
importances = model.feature_importances_
feature_names = X.columns
feature_importances = pd.DataFrame(zip(feature_names, importances), columns=['feature', 'importance']).sort_values('importance', ascending=False)

print("Feature importances:")
print(feature_importances)
