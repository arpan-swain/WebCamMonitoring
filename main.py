import cv2
import time
from sendemail import send_email
import glob


video = cv2.VideoCapture(0)
time.sleep((1))

first_frame = None
status_list=[]
img_count = 0

while True:
    status = 0
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
        # (if rectangle)only gives error
        if rectangle.any():
            status=1
            # Capture image
            cv2.imwrite(f"images/{img_count}.png", frame)
            img_count+=1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images)/2)
            image_with_object = all_images[index]

    status_list.append(status)
    new_status = status_list[-2:]
    if new_status[0] == 1 and new_status[1] == 0:
        send_email()

    cv2.imshow("My video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()