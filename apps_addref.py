# mICE Project
# Apps: Add Reference - Adds a references point into the marker file

from utils import *
from session import Session, Markerfile, CoordinateStatus
from appsx import *
import math


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

class ReferenceId(Enum):
    ORIGIN = 0
    AXIS_FEEDER = 1
    AXIS_CAMERA = 2
    AXIS_UPWARD = 3
    WARP_BACKGRID_5 = 4
    WARP_FLOORGRID_1 = 5
    DEFAULT_REFERENCE_ID_LIMIT = 6


def get_nearest_reference_point(markerfile_handler, frame_id_selected):
    mesh = markerfile_handler.get_mesh()
    lastest_ref = mesh.references[0]
    max_frame_id = 0
    for ref in mesh.references:
        if frame_id_selected >= ref.references_frame_id and ref.references_frame_id >= max_frame_id:
            lastest_ref = ref
            max_frame_id = ref.references_frame_id
    return lastest_ref


def get_data_from_reference_id_selected(ref_object, ref_id_selected):
    if ReferenceId(ref_id_selected) == ReferenceId.ORIGIN:
        return ref_object.point_origin
    elif ReferenceId(ref_id_selected) == ReferenceId.AXIS_FEEDER:
        return ref_object.axis_feeder
    elif ReferenceId(ref_id_selected) == ReferenceId.AXIS_CAMERA:
        return ref_object.axis_camera
    elif ReferenceId(ref_id_selected) == ReferenceId.AXIS_UPWARD:
        return ref_object.axis_upward
    elif ReferenceId(ref_id_selected) == ReferenceId.WARP_BACKGRID_5:
        return ref_object.warp_backgrid_5
    elif ReferenceId(ref_id_selected) == ReferenceId.WARP_FLOORGRID_1:
        return ref_object.warp_floorgrid_1
    


def get_label_from_reference_id_selected(ref_id_selected):
    if ReferenceId(ref_id_selected) == ReferenceId.ORIGIN:
        return "Origin (0,0,0)"
    elif ReferenceId(ref_id_selected) == ReferenceId.AXIS_FEEDER:
        return "Axis Feeder (X) (5,0,0)"
    elif ReferenceId(ref_id_selected) == ReferenceId.AXIS_CAMERA:
        return "Axis Camera (Z) (0,0,5)"
    elif ReferenceId(ref_id_selected) == ReferenceId.AXIS_UPWARD:
        return "Axis Upward (Y) (0,5,0)"
    elif ReferenceId(ref_id_selected) == ReferenceId.WARP_BACKGRID_5:
        return "Warp Back Grid 5 (5,5,0)"
    elif ReferenceId(ref_id_selected) == ReferenceId.WARP_FLOORGRID_1:
        return "Warp Floor Grid 1 (5,0,1)"
    

def render_reference_points(markerfile_handler, ref_id_selected, frame_id_selected):
    mesh = markerfile_handler.get_mesh()
    references_obj = get_nearest_reference_point(markerfile_handler, frame_id_selected)

    # render all references points
    for ref_id in range(ReferenceId.DEFAULT_REFERENCE_ID_LIMIT.value):
        ref_obj = get_data_from_reference_id_selected(references_obj, ref_id)

        if ref_obj.status != CoordinateStatus.SET:
            # print(f"Ref ID: {ref_id} - {get_label_from_reference_id_selected(ref_id)} - Not Set")
            continue

        if ReferenceId(ref_id) == ReferenceId.ORIGIN:
            cv2.circle(frame, (ref_obj.x, ref_obj.y), 5, (0, 0, 255), -1)
    
        if ReferenceId(ref_id) == ReferenceId.AXIS_FEEDER:
            cv2.circle(frame, (ref_obj.x, ref_obj.y), 5, (0, 255, 0), -1)
            # if origin is SET, draw a line from origin to this point
            if references_obj.point_origin.status == CoordinateStatus.SET:
                cv2.line(frame, (references_obj.point_origin.x, references_obj.point_origin.y), (ref_obj.x, ref_obj.y), (150, 150, 255), 2)

        if ReferenceId(ref_id) == ReferenceId.AXIS_CAMERA:
            cv2.circle(frame, (ref_obj.x, ref_obj.y), 5, (255, 0, 0), -1)
            # if origin is SET, draw a line from origin to this point
            if references_obj.point_origin.status == CoordinateStatus.SET:
                cv2.line(frame, (references_obj.point_origin.x, references_obj.point_origin.y), (ref_obj.x, ref_obj.y), (255, 150, 150), 2)

        if ReferenceId(ref_id) == ReferenceId.AXIS_UPWARD:
            cv2.circle(frame, (ref_obj.x, ref_obj.y), 5, (255, 255, 0), -1)
            # if origin is SET, draw a line from origin to this point
            if references_obj.point_origin.status == CoordinateStatus.SET:
                cv2.line(frame, (references_obj.point_origin.x, references_obj.point_origin.y), (ref_obj.x, ref_obj.y), (150, 255, 150), 2)

        if ReferenceId(ref_id) == ReferenceId.WARP_FLOORGRID_1:
            cv2.circle(frame, (ref_obj.x, ref_obj.y), 5, (0, 255, 255), -1)
            # check of origin, axis_feeder, axis_camera is SET
            if references_obj.point_origin.status != CoordinateStatus.SET or references_obj.axis_feeder.status != CoordinateStatus.SET or references_obj.axis_camera.status != CoordinateStatus.SET:
                return
            
            # calculate the vertical distance between this point and the axis_feeder
            vertical_distance = ref_obj.y - references_obj.axis_feeder.y

            # find slope of the line between origin to axis_camera, in degrees
            slope = math.degrees(math.atan2(references_obj.axis_camera.y - references_obj.point_origin.y, references_obj.axis_camera.x - references_obj.point_origin.x))

            # find diff x fron vertical_distance and slope
            diff_x = int(vertical_distance / math.tan(math.radians(slope)))

            #print(f"Vertical Distance: {vertical_distance}")
            #print(f"Slope: {slope}")
            #print(f"Diff X: {diff_x}")

            # draw a line from this point to (origin.x, origin.y + vertical_distance)
            cv2.line(frame, (ref_obj.x, ref_obj.y), (references_obj.point_origin.x + diff_x, references_obj.point_origin.y + vertical_distance), (150, 255, 255), 2)

            # draw a line from this point to (origin.x + diff_x, origin.y)
            cv2.circle(frame, (references_obj.point_origin.x + diff_x, references_obj.point_origin.y + vertical_distance), 5, (0, 255, 255), -1)

            # draw a line from axis_feeder, passing through this point, and stop at y = axis_camera.y, calculate the point position
            # find the slope of the line between axis_feeder and this point
            slope_feeder = math.degrees(math.atan2(ref_obj.y - references_obj.axis_feeder.y, ref_obj.x - references_obj.axis_feeder.x))
            # find the diff x from axis_feeder and slope_feeder
            diff_x_feeder = int((references_obj.axis_camera.y - references_obj.axis_feeder.y) / math.tan(math.radians(slope_feeder)))
            
            # draw a line from axis_feeder to (axis_feeder.x + diff_x_feeder, axis_camera.y)
            cv2.line(frame, (references_obj.axis_feeder.x, references_obj.axis_feeder.y), (references_obj.axis_feeder.x + diff_x_feeder, references_obj.axis_camera.y), (150, 255, 255), 2)

            # draw a line from (references_obj.axis_feeder.x + diff_x_feeder, references_obj.axis_camera.y) to axis_camera
            cv2.line(frame, (references_obj.axis_feeder.x + diff_x_feeder, references_obj.axis_camera.y), (references_obj.axis_camera.x, references_obj.axis_camera.y), (150, 255, 255), 2)


        if ReferenceId(ref_id) == ReferenceId.WARP_BACKGRID_5:
            cv2.circle(frame, (ref_obj.x, ref_obj.y), 5, (255, 0, 255), -1)
            # check of origin, axis_feeder are SET
            if references_obj.point_origin.status != CoordinateStatus.SET or references_obj.axis_feeder.status != CoordinateStatus.SET:
                return  
            
            # given the point, draw line to the axis_feeder and axis_upward
            cv2.line(frame, (ref_obj.x, ref_obj.y), (references_obj.axis_feeder.x, references_obj.axis_feeder.y), (150, 255, 255), 2) # line V
            cv2.line(frame, (ref_obj.x, ref_obj.y), (references_obj.axis_upward.x, references_obj.axis_upward.y), (150, 255, 255), 2) # line H

            # divide the line V into 5 equal parts
            point_on_vr = []
            for i in range(1, 6):
                x = int(ref_obj.x + (references_obj.axis_feeder.x - ref_obj.x) * i / 5)
                y = int(ref_obj.y + (references_obj.axis_feeder.y - ref_obj.y) * i / 5)
                point_on_vr.append((x, y))
                cv2.circle(frame, (x, y), 3, (255, 0, 255), -1)

            # divide the axis_upward to origin into 5 equal parts
            point_on_vl = []
            for i in range(1, 6):
                x = int(references_obj.axis_upward.x + (references_obj.point_origin.x - references_obj.axis_upward.x) * i / 5)
                y = int(references_obj.axis_upward.y + (references_obj.point_origin.y - references_obj.axis_upward.y) * i / 5)
                point_on_vl.append((x, y))
                cv2.circle(frame, (x, y), 3, (255, 0, 255), -1)

            # draw line from each point on vl to vr
            for i in range(5):
                cv2.line(frame, point_on_vl[i], point_on_vr[i], (150, 255, 255), 2)

            # divide the line H into 5 equal parts
            point_on_hu = []
            for i in range(1, 6):
                x = int(ref_obj.x + (references_obj.axis_upward.x - ref_obj.x) * i / 5)
                y = int(ref_obj.y + (references_obj.axis_upward.y - ref_obj.y) * i / 5)
                point_on_hu.append((x, y))
                cv2.circle(frame, (x, y), 3, (255, 0, 255), -1)

            # divide the axis_feeder to origin into 5 equal parts
            point_on_hd = []
            for i in range(1, 6):
                x = int(references_obj.axis_feeder.x + (references_obj.point_origin.x - references_obj.axis_feeder.x) * i / 5)
                y = int(references_obj.axis_feeder.y + (references_obj.point_origin.y - references_obj.axis_feeder.y) * i / 5)
                point_on_hd.append((x, y))
                cv2.circle(frame, (x, y), 3, (255, 0, 255), -1)

            # draw line from each point on hd to hu
            for i in range(5):
                cv2.line(frame, point_on_hd[i], point_on_hu[i], (150, 255, 255), 2)





            



if __name__ == '__main__':

    # Read the configuration file
    config = read_config()
    if config["version"] != Markerfile.DEFAULT_CONFIG_SUPPORTED_VERSION:
        print(f"The configuration file V.{config["version"]} is not supported (Require. V.{Markerfile.DEFAULT_CONFIG_SUPPORTED_VERSION})")
        exit()

    # Create Session
    session_id = "0a468a54fb2703ba"
    session_handler = Session(session_id)

    # Load the video file
    video_path = session_handler.get_videofile_path()
    capture_handler = cv2.VideoCapture(video_path)

    # Check if the video file is opened
    if not capture_handler.isOpened():
        print(f"Error: Unable to open the video file {video_path}")
        exit()

    # Get the total frame of the video
    frame_total = int(capture_handler.get(cv2.CAP_PROP_FRAME_COUNT))

    # Load the marker file
    if (session_handler.is_markerfile_founded()):
        print("Marker file found. Loading marker file")
        markerfile_handler = session_handler.load_markerfile()
        print(f"Marker file timestamp: {markerfile_handler.get_timestamp_lastupdated()}")
    else:
        print("Marker file not found. Creating new marker file")
        markerfile_handler = Markerfile(session_id, frame_total)
        session_handler.save_markerfile(markerfile_handler)

    # Check if the markerfile version is supported
    if not markerfile_handler.is_version_supported(config["version"]):
        print(f"The marker file V.{markerfile_handler.get_version()} is not supported (From Config.json, Require. V.{config["version"]})")
        exit()

    # Check if the mesh size is the same as the video frame
    if markerfile_handler.get_mesh().frame_total != frame_total:
        print(f"The marker file frame total {markerfile_handler.get_mesh().frame_total} is not the same as the video frame total {frame_total}")
        exit()

    # Define the window name, also use it as tag for using in CV
    window_name = f"{session_id} - mICE Video Marker"

    # Create a window
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # Set the mouse callback function
    cv2.setMouseCallback(window_name, on_clicked)

    frame_id_current = 0
    # marker_id_selected = 0
    ref_id_selected = 0

    saved_frame = None
    flag_pause = True

    while True:
        

        if flag_pause:
            if saved_frame is None:
                ret, saved_frame = capture_handler.read()
            frame = saved_frame.copy()
        else:
            ret, frame = capture_handler.read()

        frame_id_current = int(capture_handler.get(cv2.CAP_PROP_POS_FRAMES)) - 1

        # Render frame info
        render_ui_frame_id(frame, frame_id_current, frame_total)

        # Render reference points
        render_reference_points(markerfile_handler, ref_id_selected, frame_id_current)

        if (global_flag_onclick_left or global_flag_onclick_right or global_flag_onclick_middle):
            if not flag_pause:
                # display message that click is disabled during playback
                log("Click is disabled during playback")
                cv2.putText(frame, "Click is disabled during playback", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            else:
                mesh = markerfile_handler.get_mesh()
                references_obj = get_nearest_reference_point(markerfile_handler, frame_id_current)
                ref_obj = get_data_from_reference_id_selected(references_obj, ref_id_selected)

                if global_flag_onclick_left:
                    log("Left Click")
                    log(global_var_onclick_point)
                    ref_obj.x = global_var_onclick_point["x"]
                    ref_obj.y = global_var_onclick_point["y"]
                    ref_obj.status = CoordinateStatus.SET
  
                if global_flag_onclick_right:
                    log(f"Right Click")
                    log(global_var_onclick_point)
                    ref_obj.status = CoordinateStatus.NOT_ASSIGNED
 
                if global_flag_onclick_middle:
                    log(f"Middlet Click")
                    log(global_var_onclick_point)
 
            global_flag_onclick_left = False
            global_flag_onclick_right = False
            global_flag_onclick_middle = False


        # Display the frame
        cv2.imshow(window_name, frame)

        # Wait for a key press, q to exit, space to start/stop the video (keep playing current frame)
        key = cv2.waitKey(1) & 0xFF
        if key in [ord('q'),ord('Q')]:
            if(key == ord('q')):
                log("Saving marker file")
                session_handler.save_markerfile(markerfile_handler)
                log("Marker file saved.")
                log("Exit.")
                exit()
            else:
                log("Force Exit. No Saving.")
                exit()
            
        elif key == ord('s'):
            log("Saving marker file")
            session_handler.save_markerfile(markerfile_handler)
            log("Marker file saved.")

        elif key in [ord(' '),ord('Z'),ord('z'),ord('x'),ord('v'),ord('b')]:
            if key == ord(' '):
                is_on_seeking = False
                if flag_pause:
                    flag_pause = False
                    saved_frame = None
                else:
                    flag_pause = True
                frame_id_current = int(capture_handler.get(cv2.CAP_PROP_POS_FRAMES)) - 1

            if key == ord('Z'):
                frame_id_current = 0

            if key == ord('z'):
                frame_id_current -= 240

            if key == ord('x'):
                frame_id_current -= 1

            if key == ord('v'):
                frame_id_current += 1

            if key == ord('b'):
                frame_id_current += 240

            capture_handler.set(cv2.CAP_PROP_POS_FRAMES, frame_id_current)
            saved_frame = None

        elif key in [ord('1'),ord('2'),ord('3'),ord('4'),ord('5'),ord('6')]:
            ref_id_selected = key - ord('1')
            print(f"Selected Ref ID: {ref_id_selected} - {get_label_from_reference_id_selected(ref_id_selected)}")
            