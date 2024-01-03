import csv
import cv2
import numpy as np
import os
import mediapipe as mp

# Initialize MediaPipe Holistic.
mp_holistic = mp.solutions.holistic

landmark_description = [
"nose", "left_eye_inner", "left_eye", "left_eye_outer", 
"right_eye_inner", "right_eye", "right_eye_outer", "left_ear", 
"right_ear", "mouth_left", "mouth_right", "left_shoulder", 
"right_shoulder", "left_elbow", "right_elbow", "left_wrist", 
"right_wrist", "left_pinky", "right_pinky", "left_index", 
"right_index", "left_thumb", "right_thumb", "left_hip", 
"right_hip", "left_knee", "right_knee", "left_ankle", 
"right_ankle", "left_heel", "right_heel", "left_foot_index", 
"right_foot_index"
]

# Function to calculate the Euclidean distance between two points.
def calculate_distance(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.linalg.norm(a-b)

# Function to calculate the angle between three points.
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

# Process images from a folder, analyze them, and write data to a CSV file.
def process_images_from_folder(folder_path, writer, label):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check for image files.
            image = cv2.imread(file_path)
            results = mp_holistic.Holistic(static_image_mode=True, model_complexity=2,
                                           enable_segmentation=True, refine_face_landmarks=True).process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                row_data = {'file_name': file_name, 'label': label}
                for i, landmark in enumerate(landmarks):
                    # Record landmark positions and visibility with descriptive names
                    row_data[f'{landmark_description[i]}_x'] = landmark.x
                    row_data[f'{landmark_description[i]}_y'] = landmark.y
                    row_data[f'{landmark_description[i]}_z'] = landmark.z
                    row_data[f'{landmark_description[i]}_visibility'] = landmark.visibility
                
                # Calculate and record distances between each pair of landmarks with descriptive names.
                for i in range(len(landmarks)):
                    for j in range(i+1, len(landmarks)):
                        distance = calculate_distance([landmarks[i].x, landmarks[i].y, landmarks[i].z],
                                                      [landmarks[j].x, landmarks[j].y, landmarks[j].z])
                        row_data[f'distance_between_{landmark_description[i]}_and_{landmark_description[j]}'] = distance
                        
                        # Calculate and record angles among triplets of landmarks with descriptive names.
                        if i < len(landmarks) - 2 and j < len(landmarks) - 1:
                            for k in range(j+1, len(landmarks)):
                                angle = calculate_angle([landmarks[i].x, landmarks[i].y, landmarks[i].z],
                                                        [landmarks[j].x, landmarks[j].y, landmarks[j].z],
                                                        [landmarks[k].x, landmarks[k].y, landmarks[k].z])
                                row_data[f'angle_between_{landmark_description[i]}_{landmark_description[j]}_{landmark_description[k]}'] = angle
                
                writer.writerow(row_data)  # Write the row data for this image.