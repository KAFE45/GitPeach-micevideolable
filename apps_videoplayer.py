# mICE Project
# Apps : Example of how to play video using OpenCV

from utils import *


def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    tick = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video Player', frame)
        tock = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        log(total_frame, current_frame)

        recorded_fps = cap.get(cv2.CAP_PROP_FPS)
        playback_fps = 1/(tock-tick)
        log(recorded_fps, playback_fps)

        tick = tock
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video_path = "dataset/f5aaf7aa708eca80.MOV"
    play_video(video_path)