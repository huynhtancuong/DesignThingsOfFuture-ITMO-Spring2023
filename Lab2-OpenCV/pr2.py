import cv2
import time

cap = cv2.VideoCapture('cam_video.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    ret, thresh = cv2.threshold(gray, 105, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)



    if len(contours) > 0:
        # find the biggest contour
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # calculate distance between the center of the contour and the center of the frame
        center_x = int(x + w / 2)
        center_y = int(y + h / 2)

        frame_height, frame_width = frame.shape[:2]
        frame_center_x = frame_width // 2
        frame_center_y = frame_height // 2

        distance_x = abs(center_x - frame_center_x)
        distance_y = abs(center_y - frame_center_y)
        distance   = int((distance_x**2 + distance_y**2)**0.5)

        # draw a line between the center of the contour and the center of the frame
        cv2.line(frame, (frame_center_x, frame_center_y), (center_x, center_y), (255, 255, 0), 2)

        # show the distance between the center of the contour and the center of the frame
        text = 'X: ' + str(x) + ' Y: ' + str(y) + ' Distance: ' + str(distance)
        cv2.putText(frame, text, (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('frame', frame)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    # time.sleep(0.1)


cap.release()
cv2.destroyAllWindows()
