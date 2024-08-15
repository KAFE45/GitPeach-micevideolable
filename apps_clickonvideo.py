# mICE Project
# Apps: Click on Video - Example of how to manage click events on OpenCV window

from utils import *
from session import Session, Markerfile

# define point for rendering intop frame
points = []

def on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        points.append((x, y))

    if event == cv2.EVENT_RBUTTONDOWN:
        if len(points) > 0:
            points.pop()

    if event == cv2.EVENT_MBUTTONDOWN:
        points.clear()


def render_points(frame, points):
    for point in points:
        cv2.circle(frame, point, 3, (0, 0, 255), -1)

def render_frame_id(frame, frame_id, frame_total):
    cv2.putText(frame, f'{frame_total} : {frame_id}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)


if __name__ == '__main__':

    # Read the configuration file
    config = read_config()

    # Create Session
    session_id = "f5aaf7aa708eca80"
    session_handler = Session(session_id)

    # Open the video file
    cap = cv2.VideoCapture(session_handler.get_videofile_path())

    # Define the window name, also use it as tag for using in CV
    window_name = f"{session_id} - mICE Video Marker"

    # Create a window
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # Set the mouse callback function
    cv2.setMouseCallback(window_name, on_click)

    frame_id = 0
    frame_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    flag_pause = False


    while True:
        # Check if the video is paused, if so, then keep playing the current frame
        if flag_pause:
            frame = original_frame.copy()
        else:
            ret, frame = cap.read()
        
        frame_id = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        # If the frame was not read, then we have reached the end of the video
        if not ret:
            break

        # Render the points
        render_points(frame, points)

        # Render the frame id
        render_frame_id(frame, frame_id, frame_total)


        # Display the frame
        cv2.imshow(window_name, frame)

        # Wait for a key press, q to exit, space to start/stop the video (keep playing current frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):
            if flag_pause:
                flag_pause = False
            else:
                flag_pause = True
                frame_id = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
                # get from from the frame_id
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
                ret, original_frame = cap.read()

    # Release the video capture object
    cap.release()

    # Destroy the window
    cv2.destroyAllWindows()

