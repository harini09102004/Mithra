import os
import pickle
import mediapipe as mp
import cv2

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = './data'

data = []
labels = []

# Check if the data directory exists
if not os.path.exists(DATA_DIR):
    print(f"Error: The directory {DATA_DIR} does not exist.")
else:
    for dir_ in os.listdir(DATA_DIR):
        dir_path = os.path.join(DATA_DIR, dir_)
        
        # Check if the directory is indeed a directory
        if os.path.isdir(dir_path):
            for img_path in os.listdir(dir_path):
                # Construct the full image path
                img_full_path = os.path.join(dir_path, img_path)
                
                # Read the image
                img = cv2.imread(img_full_path)
                if img is None:  # Check if the image was read successfully
                    print(f"Warning: Could not read image {img_full_path}. Skipping...")
                    continue

                # Convert the image to RGB
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # Process the image with MediaPipe Hands
                results = hands.process(img_rgb)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        data_aux = []  # Reset data_aux for each hand
                        x_ = []
                        y_ = []

                        # Collect landmark coordinates
                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y

                            x_.append(x)
                            y_.append(y)

                        # Normalize and store the landmark coordinates
                        for i in range(len(x_)):  # Iterate over the indices of x_
                            data_aux.append(x_[i] - min(x_))  # Correctly index into x_ and y_
                            data_aux.append(y_[i] - min(y_))

                        # Append the data and label
                        data.append(data_aux)
                        labels.append(dir_)
                else:
                    print(f"No hands detected in image: {img_full_path}")

# Save the data to a pickle file
with open('data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

print("Data processing complete. Data saved to 'data.pickle'.")
