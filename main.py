import cv2 as cv
import numpy as np
import time

vid = cv.VideoCapture(0)
vid.set(cv.CAP_PROP_FRAME_WIDTH, 640)
vid.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize background
ret, background = vid.read()
background = np.flip(background, axis=1)
last_bg_update = time.time()

# Define HSV range for blue
lower_blue = np.array([94, 80, 2])
upper_blue = np.array([126, 255, 255])

print("Blue invisibility cloak with background refresh every 10s")

while True:
    ret, frame = vid.read()
    if not ret:
        break

    frame = np.flip(frame, axis=1)

    current_time = time.time()
    #BG Refreshing after every 10 seconds 
    # We can make it to stay the same by replacing the lower code and initilize the bg outside the loop
    if current_time - last_bg_update > 10:
        print("Refreshing background...")
        ret, background = vid.read()
        background = np.flip(background, axis=1)
        last_bg_update = current_time

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    mask = cv.inRange(hsv, lower_blue, upper_blue)
    mask_inv = cv.bitwise_not(mask)

    res1 = cv.bitwise_and(frame, frame, mask=mask_inv)
    res2 = cv.bitwise_and(background, background, mask=mask)

    final_output = cv.addWeighted(res1, 1, res2, 1, 0)

    cv.imshow("Invisible Blue Cloak", final_output)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()
