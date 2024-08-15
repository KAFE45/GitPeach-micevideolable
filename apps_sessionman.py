# mICE Project
# Apps: Session Manager - Example of how to manage session files by ID 
#       using the Session classes


from utils import *
from session import Session, Markerfile


if __name__ == '__main__':
    session_id = "f5aaf7aa708eca80"
    session_handler = Session(session_id)

    # optional: set the video file directory
    # session_handler.set_videofile_dir()

    log(session_handler.get_videofile_dir())
    log(session_handler.get_videofile_path())
    log(session_handler.is_videofile_founded())
    
    # optional: set the marker file directory
    # session_handler.set_markerfile_dir()

    log(session_handler.get_markerfile_dir())
    log(session_handler.get_markerfile_path())
    log(session_handler.is_markerfile_founded())

    marker = Markerfile()
    log(marker)
    log(marker.get_updated_timestamp())

    # Save the marker object
    session_handler.save_markerfile(marker)

    # Load the marker object
    loaded_marker = session_handler.load_markerfile()
    log(loaded_marker)
    log(loaded_marker.get_updated_timestamp())

