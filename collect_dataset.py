import cv2


ip_address = ""  # Replace with the IP address from the IP Webcam app
# url = f"http://192.168.54.239:8080/video"

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

n = 1700
while True:
    ret, frame = cap.read()

    cv2.imshow("IP Camera Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('s'):

        cv2.imwrite("dataset2/accident/zxy"+str(n)+".jpg", frame)
        n = n + 1
        print("cature")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()