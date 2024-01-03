import csv
import cv2
import numpy as np
import os
import mediapipe as mp
from preprocessing import process_images_from_folder, landmark_description

def data_acquisition():
    base_folder_path = "C:\\Users\\user\\Desktop\\project\\BigProject\\data"  # Base folder containing sub-folders.
    csv_file = "C:\\Users\\user\\Desktop\\project\\BigProject\\data\\output.csv"  # Path to save the CSV file.


    # Dynamically create CSV columns based on the expected number of landmarks, distances, and angles.
    csv_columns = ['file_name', 'label'] + [f'{name}_{dim}' for name in landmark_description for dim in ['x', 'y', 'z', 'visibility']]  # Landmark positions and visibility.
    csv_columns += [f'distance_between_{landmark_description[i]}_and_{landmark_description[j]}' for i in range(len(landmark_description)) for j in range(i+1, len(landmark_description))]  # Distances.
    csv_columns += [f'angle_between_{landmark_description[i]}_{landmark_description[j]}_{landmark_description[k]}' for i in range(len(landmark_description)) for j in range(i+1, len(landmark_description)) for k in range(j+1, len(landmark_description))]  # Angles.

    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        
        # Assign numeric labels based on sub-folder names
        sub_folders = [f.name for f in os.scandir(base_folder_path) if f.is_dir()]
        label_dict = {name: idx for idx, name in enumerate(sub_folders)}

        # Process each sub-folder
        for sub_folder in sub_folders:
            full_folder_path = os.path.join(base_folder_path, sub_folder)
            process_images_from_folder(full_folder_path, writer, label_dict[sub_folder])

if __name__ == "__main__":
    data_acquisition()
