# mICE Project
# AppsX - Common UI callbacks and flags

from utils import *
from session import Session, Markerfile, CoordinateStatus

# define point for rendering intop frame
points = []

global_flag_onclick_left = False
global_flag_onclick_right = False
global_flag_onclick_middle = False

global_var_onclick_point = {"x": 0, "y": 0}

global_flag_autosave_enabled = True
global_flag_autosave_calling = False


def on_clicked(event, x, y, flags, param):
    global global_flag_onclick_left
    global global_flag_onclick_right
    global global_flag_onclick_middle
    global global_var_onclick_point

    if event == cv2.EVENT_LBUTTONDOWN:
        global_flag_onclick_left = True
        global_var_onclick_point["x"] = x
        global_var_onclick_point["y"] = y

    if event == cv2.EVENT_RBUTTONDOWN:
        global_flag_onclick_right = True
        global_var_onclick_point["x"] = x
        global_var_onclick_point["y"] = y

    if event == cv2.EVENT_MBUTTONDOWN:
        global_flag_onclick_middle = True
        global_var_onclick_point["x"] = x
        global_var_onclick_point["y"] = y


def render_points(frame, points):
    for point in points:
        cv2.circle(frame, point, 3, (0, 0, 255), -1)


def render_ui_frame_id(frame, frame_id, frame_total):
    cv2.putText(frame, f'{frame_total} : {frame_id}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)


class MarkerId(Enum):
    PELLET = 0
    NOSETIP = 1
    FINGER_TIP_RIGHT = 2
    FINGER_THUMB_RIGHT = 3
    PALM_RIGHT = 4
    FINGER_TIP_LEFT = 5
    DEFAULT_MARKER_ID_LIMIT = 6


def get_data_from_marker_id_selected(marker_object, marker_id_selected):
    if MarkerId(marker_id_selected) == MarkerId.PELLET:
        return marker_object.pellet
    elif MarkerId(marker_id_selected) == MarkerId.NOSETIP:
        return marker_object.nosetip
    elif MarkerId(marker_id_selected) == MarkerId.FINGER_TIP_RIGHT:
        return marker_object.finger_tip_right
    elif MarkerId(marker_id_selected) == MarkerId.FINGER_THUMB_RIGHT:
        return marker_object.finger_thumb_right
    elif MarkerId(marker_id_selected) == MarkerId.PALM_RIGHT:
        return marker_object.palm_right
    elif MarkerId(marker_id_selected) == MarkerId.FINGER_TIP_LEFT:
        return marker_object.finger_tip_left
    else:
        return None
    

def get_label_from_marker_id_selected(marker_id_selected):
    if MarkerId(marker_id_selected) == MarkerId.PELLET:
        return "Pellet"
    elif MarkerId(marker_id_selected) == MarkerId.NOSETIP:
        return "Nose Tip"
    elif MarkerId(marker_id_selected) == MarkerId.FINGER_TIP_RIGHT:
        return "Right Finger Tip"
    elif MarkerId(marker_id_selected) == MarkerId.FINGER_THUMB_RIGHT:
        return "Right Thumb"
    elif MarkerId(marker_id_selected) == MarkerId.PALM_RIGHT:
        return "Right Palm"
    elif MarkerId(marker_id_selected) == MarkerId.FINGER_TIP_LEFT:
        return "Left Finger Tip"
    else:
        return None
    

def autosave_markerfile(session_handler, markerfile_handler, period_sec=60):
    global global_flag_autosave_calling
    counter = 0
    while global_flag_autosave_enabled:
        time.sleep(1)
        counter += 1
        if counter >= period_sec:
            counter = 0
            global_flag_autosave_calling = True



def get_coordinate_obj(mesh, frame_id, marker_id):
    marker_object_on_frame = mesh.markers[frame_id]
    selected_marker_object = get_data_from_marker_id_selected(marker_object_on_frame, marker_id)
    return selected_marker_object



def is_set_marker_founded(markerfile_handler, marker_id_selected, frame_id_selected):
    mesh = markerfile_handler.get_mesh()
    current_coordinate = get_coordinate_obj(mesh, frame_id_selected, marker_id_selected)
    return current_coordinate.status == CoordinateStatus.SET

