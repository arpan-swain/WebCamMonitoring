import cv2
import time
from sendemail import send_email


video = cv2.VideoCapture(0)
time.sleep((1))

first_frame = None

while True:
    check, frame = video.read()
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_gau = cv2.GaussianBlur(gray_img,(21,21), 0)


    if first_frame is None:
        first_frame = gray_gau

    delta = cv2.absdiff(first_frame, gray_gau)


    thresh_frame = cv2.threshold(delta, 50, 255, cv2.THRESH_BINARY)[1]
    # remove noise
    dilate = cv2.dilate(thresh_frame, None, iterations=2)


    #contours around the object
    contours, check = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # remove false contours
    for contour in contours:
        if cv2.contourArea(contour)<10000:
            continue
        x,y,w,h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), thickness=3)
        if rectangle:
            send_email()

    cv2.imshow("My video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()