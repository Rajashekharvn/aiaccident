


import cv2
import time
import numpy as np
from collections import deque
from tensorflow.keras.models import load_model
from send_notification import send_notif

# Load model
model = load_model("keras_model.h5")  # Replace with your actual model file
class_names = ["Normal", "Accident"]  # Adjust according to your dataset

# Settings
target_class_index = 1  # index of "Accident" class (Class 2)
confidence_threshold = 0.7
duration_seconds = 5
frame_rate = 10  # how many frames per second to process
url = f"http://192.0.0.4:8080/video"
# Setup video
cap = cv2.VideoCapture(url)  # Use 0 for webcam
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Store results over time
results_buffer = deque()

start_time = time.time()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize and preprocess frame (match model input size)
        img = cv2.resize(frame, (224, 224))  # Adjust depending on your model
        img = img / 255.0
        img = np.expand_dims(img, axis=0)

        # Predict
        preds = model.predict(img, verbose=0)[0]
        predicted_class = np.argmax(preds)
        confidence = preds[predicted_class]

        # Store prediction if confident
        current_time = time.time()
        results_buffer.append((current_time, predicted_class, confidence))

        # Remove old predictions
        while results_buffer and (current_time - results_buffer[0][0] > duration_seconds):
            results_buffer.popleft()

        # Count class 2 (target) predictions
        class_2_votes = sum(1 for t, cls, conf in results_buffer if cls == target_class_index and conf > confidence_threshold)
        total_votes = len(results_buffer)

        # Display live info
        status_text = f"Class: {class_names[predicted_class]} ({confidence:.2f})"
        vote_text = f"Class 2 Votes: {class_2_votes}/{total_votes}"
        if class_2_votes >= total_votes:
            send_notif("accident detected")

            cv2.imshow("Live Classification", frame)
            time.sleep(5)
            exit()
        if class_2_votes > total_votes / 2:
            final_decision = ">> ALERT: CLASS 2 DETECTED <<"  
            time.sleep(5)
            
            
            
        else:
            final_decision =""


        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, vote_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, final_decision, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Live Classification", frame)

        # Wait according to frame_rate
        if cv2.waitKey(int(1000 / frame_rate)) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
