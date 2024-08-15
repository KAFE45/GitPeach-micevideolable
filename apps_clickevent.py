# mICE Project
# Apps: Click Event - Example of how to manage click events on OpenCV window

from utils import *

img = np.zeros((512, 512, 3), np.uint8)


def on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        
        # remove the previous curcle before drawing a new one
        img[:] = 0

        # draw a circle on the image at the clicked point
        cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
        cv2.imshow('Click Event Example', img)



if __name__ == '__main__':

    # Read the configuration file
    config = read_config

    # Create a window
    cv2.namedWindow('Click Event Example')

    # Set the mouse callback function
    cv2.setMouseCallback('Click Event Example', on_click)

    # Display the window
    cv2.imshow('Click Event Example', np.zeros((512, 512, 3), np.uint8))

    # Wait for a key press
    cv2.waitKey(0)

    # Destroy the window
    cv2.destroyAllWindows()

