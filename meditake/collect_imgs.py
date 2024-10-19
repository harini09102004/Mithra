import os
import cv2

# Define the directory to save collected images
DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Define the number of classes 
number_of_classes = 2  # 0 for not taking medication, 1 for taking medication
dataset_size = 100  # Number of images to capture per class

# Initialize video capture (use appropriate camera index)
cap = cv2.VideoCapture(0)  # Change the index based on your setup

# Loop over each class
for j in range(number_of_classes):
    class_dir = os.path.join(DATA_DIR, str(j))
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    action = "taking medication" if j == 1 else "not taking medication"
    print(f'Collecting data for class {action}')

    # Wait for user to get ready
    done = False
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        cv2.putText(frame, f'Press "Q" to start collecting data for {action}!', (100, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        cv2.imshow('frame', frame)
        cv2.waitKey(25)  # Display the frame for a brief moment

        # Save the captured frame to the corresponding class directory
        image_path = os.path.join(class_dir, f'{counter}.jpg')
        cv2.imwrite(image_path, frame)

        print(f'Captured {counter + 1}/{dataset_size} images for {action}')
        counter += 1

# Release the video capture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
