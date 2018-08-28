# import the necessary packages
import cv2
import opencv_homography_lib as hl

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False

        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)


# construct the argument parser and parse the arguments
imagepath = './plainDoge.jpg'

# load the image, clone it, and setup the mouse callback function
image = cv2.imread(imagepath)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        image = clone.copy()

    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break

# if there are two reference points, then crop the region of interest
# from teh image and display it
print(refPt)
if len(refPt) == 2:
    roi = clone[refPt[1][1]:refPt[0][1], refPt[0][0]:refPt[1][0]]

roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
cap = cv2.VideoCapture(0)

while True:
    try:
        ok, img1 = cap.read()
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img, _ = hl.surf_homography(roi, img1)
        cv2.imshow("correspondence", img)

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    except Exception as e:
        print(e)

# close all open windows
cv2.destroyAllWindows()
