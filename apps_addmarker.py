# mICE Project
# Apps: Add Marker - Example of how to add marker on video


from utils import *
from session import Session, Markerfile, CoordinateStatus
from appsx import *



def render_ui_selected_marker(frame, markerfile_handler, frame_id_selected, marker_id_selected, isAllMarkerRendered=False):
    mesh = markerfile_handler.get_mesh()
    if frame_id_selected < mesh.frame_total:
        all_marker_object_on_frame = mesh.markers[frame_id_selected]

        # Render all maeker on frame
        if isAllMarkerRendered:
            for marker_id in range(MarkerId.DEFAULT_MARKER_ID_LIMIT.value):
                merker_obj = get_data_from_marker_id_selected(all_marker_object_on_frame, marker_id)
                if merker_obj.status == CoordinateStatus.SET or merker_obj.status == CoordinateStatus.ESTIMATED:
                    cv2.circle(frame, (merker_obj.x, merker_obj.y), 4, (200, 200, 255), -1)

        selected_marker_object = get_data_from_marker_id_selected(all_marker_object_on_frame, marker_id_selected)

        #print(f"Selected Frame ID: {frame_id_selected}")
        #print(f"Selected Marker ID: {marker_id_selected}")
        #print(f"All Marker Object on Frame: {all_marker_object_on_frame}")
        #print(f"Selected Marker Object: {selected_marker_object}")

        cv2.putText(frame, f"Marker: {get_label_from_marker_id_selected(marker_id_selected)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (92, 92, 252), 2, cv2.LINE_AA)


        if selected_marker_object.status == CoordinateStatus.NOT_ASSIGNED:
            cv2.putText(frame, "N/A", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (40, 40, 40), 2, cv2.LINE_AA)
        if selected_marker_object.status == CoordinateStatus.OFF_SCREEN:
            cv2.putText(frame, "OFFSCREEN", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 100), 2, cv2.LINE_AA)
        if selected_marker_object.status == CoordinateStatus.ESTIMATED:
            cv2.putText(frame, f"~ {(selected_marker_object.x, selected_marker_object.y)} (estimated)", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 200), 2, cv2.LINE_AA)
            cv2.circle(frame, (selected_marker_object.x, selected_marker_object.y), 4, (0, 255, 0), -1)
        if selected_marker_object.status == CoordinateStatus.SET:
            cv2.putText(frame, f"@ {(selected_marker_object.x, selected_marker_object.y)}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.circle(frame, (selected_marker_object.x, selected_marker_object.y), 4, (0, 0, 255), -1)


def render_ui_selected_marker_history(frame, markerfile_handler, frame_id_selected, marker_id_selected, history_frame=10, isDrawOnlySetEstimate=True):

    if history_frame < 1:
        return

    # rainbow color code for draing history line
    #color_code = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]

    # generate rainbow color code for drawing history line, size of history_frame, using cv2 color format
    color_code = []
    for i in range(history_frame):
        color_code.append(tuple([int(c*255) for c in hsv_to_rgb(i/history_frame, 1, 1)]))

    mesh = markerfile_handler.get_mesh()
    # get latest histora_frame from frame_id_selected
    history_frame_id = frame_id_selected - history_frame
    if history_frame_id < 0:
        history_frame_id = 0

    # check if the selected marker is SET or ESTIMATED
    if isDrawOnlySetEstimate: 
        all_marker_object_on_frame = mesh.markers[frame_id_selected]
        selected_marker_object = get_data_from_marker_id_selected(all_marker_object_on_frame, marker_id_selected)
        if selected_marker_object.status not in [CoordinateStatus.SET, CoordinateStatus.ESTIMATED]:
            return
    
    # draw line and point for each history frame
    for i in range(frame_id_selected, history_frame_id, -1):
        all_marker_object_on_frame_head = mesh.markers[i]
        all_marker_object_on_frame_tail = mesh.markers[i-1]
        head_marker_object = get_data_from_marker_id_selected(all_marker_object_on_frame_head, marker_id_selected)
        tail_marker_object = get_data_from_marker_id_selected(all_marker_object_on_frame_tail, marker_id_selected)

        if (head_marker_object.status in [CoordinateStatus.SET, CoordinateStatus.ESTIMATED]) and (tail_marker_object.status in [CoordinateStatus.SET, CoordinateStatus.ESTIMATED]):
            cv2.line(frame, (tail_marker_object.x, tail_marker_object.y), (head_marker_object.x, head_marker_object.y), color_code[i%history_frame], 2)
            cv2.circle(frame, (head_marker_object.x, head_marker_object.y), 2, color_code[i%history_frame], -1)
            cv2.circle(frame, (tail_marker_object.x, tail_marker_object.y), 2, color_code[i%history_frame], -1)




def run_marker_regression(markerfile_handler, marker_id_selected, frame_id_selected, removeMode=False):

    mesh = markerfile_handler.get_mesh()
    
    current_coordinate = get_coordinate_obj(mesh, frame_id_selected, marker_id_selected)
    if current_coordinate.status == CoordinateStatus.SET:
        print(f"SKIP - Regression for {get_label_from_marker_id_selected(marker_id_selected)} at frame {frame_id_selected} skipped, It set already.")
    else:
        print(f"Starting Regression for {get_label_from_marker_id_selected(marker_id_selected)} at frame {frame_id_selected}...")
       
        # scan on previous frame until find the set or offscreen or reach the first frame
        previous_frame_id = frame_id_selected - 1
        while previous_frame_id > 0:
            previous_coordinate = get_coordinate_obj(mesh, previous_frame_id, marker_id_selected)
            if previous_coordinate.status == CoordinateStatus.SET:
                break
            if previous_coordinate.status == CoordinateStatus.OFF_SCREEN:
                break
            previous_frame_id -= 1
        
        # scan on next frame until find the set or offscreen or reach the last frame
        next_frame_id = frame_id_selected + 1
        while next_frame_id < mesh.frame_total-1:
            next_coordinate = get_coordinate_obj(mesh, next_frame_id, marker_id_selected)
            if next_coordinate.status == CoordinateStatus.SET:
                break
            if next_coordinate.status == CoordinateStatus.OFF_SCREEN:
                break
            next_frame_id += 1

        log(previous_frame_id, next_frame_id)
        head_frame_id = previous_frame_id
        tail_frame_id = next_frame_id
        head_coordinate = get_coordinate_obj(mesh, head_frame_id, marker_id_selected)
        tail_coordinate = get_coordinate_obj(mesh, tail_frame_id, marker_id_selected)

        print("Regression Checking")
        print(f"  From {previous_frame_id:8d} : {head_coordinate.status}")
        print(f"  To   {next_frame_id:8d} : {tail_coordinate.status}")

        if head_coordinate.status != tail_coordinate.status:
            print(f" * SKIP Regression - Head and Tail status are not matched.")
            return

        if removeMode:
            print(f" * Removing merker...")
            for i in range(head_frame_id, tail_frame_id+1):
                current_coord = get_coordinate_obj(mesh, i, marker_id_selected)
                current_coord.status = CoordinateStatus.NOT_ASSIGNED
        elif head_coordinate.status == CoordinateStatus.OFF_SCREEN:
            print(f" * OFF_SCREEN filling...")
            for i in range(head_frame_id, tail_frame_id+1):
                current_coord = get_coordinate_obj(mesh, i, marker_id_selected)
                current_coord.status = CoordinateStatus.OFF_SCREEN
        else:
            print(f" * Estimating...")
            # perform linear regression
            x1 = head_coordinate.x
            y1 = head_coordinate.y
            x2 = tail_coordinate.x
            y2 = tail_coordinate.y

            dx = x2 - x1
            dy = y2 - y1
            dt = tail_frame_id - head_frame_id

            for i in range(head_frame_id+1, tail_frame_id):
                current_coord = get_coordinate_obj(mesh, i, marker_id_selected)
                current_coord.status = CoordinateStatus.ESTIMATED
                current_coord.x = int(x1 + dx * (i - head_frame_id) / dt)
                current_coord.y = int(y1 + dy * (i - head_frame_id) / dt)

                

        print(f" * Regression done")


def run_delete_similar_marker(markerfile_handler, marker_id_selected, frame_id_selected):
    # get current frame status
    mesh = markerfile_handler.get_mesh()
    current_coordinate = get_coordinate_obj(mesh, frame_id_selected, marker_id_selected)

    # scan on left frame while the status is the same
    left_frame_id = frame_id_selected - 1
    while left_frame_id > 0:
        left_coordinate = get_coordinate_obj(mesh, left_frame_id, marker_id_selected)
        if left_coordinate.status != current_coordinate.status:
            break
        left_frame_id -= 1

    # scan on right frame while the status is the same
    right_frame_id = frame_id_selected + 1
    while right_frame_id < mesh.frame_total-1:
        right_coordinate = get_coordinate_obj(mesh, right_frame_id, marker_id_selected)
        if right_coordinate.status != current_coordinate.status:
            break
        right_frame_id += 1
    
    # set all frame from left to right to NOT_ASSIGNED
    for i in range(left_frame_id+1, right_frame_id):
        current_coord = get_coordinate_obj(mesh, i, marker_id_selected)
        current_coord.status = CoordinateStatus.NOT_ASSIGNED




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
    marker_id_selected = 0

    saved_frame = None
    flag_pause = True

    # start Autosaving thread, calling every 1 mins
    autosave_thread = Thread(target=autosave_markerfile, args=(session_handler, markerfile_handler))
    autosave_thread.start()

    is_on_seeking = False
    flag_is_set_marker_founded = False

    history_frame_render = 10

    while True:
        
        # Check if the video is paused, if so, then keep playing the current frame
        if is_on_seeking:
            if flag_is_set_marker_founded:
                is_on_seeking = False
                flag_is_set_marker_founded = False
                flag_pause = True
                saved_frame = None
                capture_handler.set(cv2.CAP_PROP_POS_FRAMES, frame_id_current)

        if flag_pause:
            if saved_frame is None:
                ret, saved_frame = capture_handler.read()
            frame = saved_frame.copy()
        else:
            ret, frame = capture_handler.read()

        frame_id_current = int(capture_handler.get(cv2.CAP_PROP_POS_FRAMES)) - 1

        # Render frame info
        render_ui_frame_id(frame, frame_id_current, frame_total)

        # if flag_global_autosave_calling is True, then show saving on frame's center and saving markerfile
        if global_flag_autosave_calling:
            log("Auto saving...")

            # Display message on the frame, at center
            cv2.putText(frame, "Auto Saving...", (int(frame.shape[1]/2)-200, int(frame.shape[0]/2)), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow(window_name, frame)
            k=cv2.waitKey(10) & 0XFF
            
            session_handler.save_markerfile(markerfile_handler)
            global_flag_autosave_calling = False
            log("Auto save done.")
            continue

        # Render the selected marker history
        render_ui_selected_marker_history(frame, markerfile_handler, frame_id_current , marker_id_selected, history_frame=history_frame_render)

        # Render the selected marker
        render_ui_selected_marker(frame, markerfile_handler, frame_id_current , marker_id_selected, isAllMarkerRendered=True)

        # check of set marker founded on this frame
        if (is_on_seeking):
            flag_is_set_marker_founded = is_set_marker_founded(markerfile_handler, marker_id_selected, frame_id_current)


        if (global_flag_onclick_left or global_flag_onclick_right or global_flag_onclick_middle):
            if not flag_pause:
                # display message that click is disabled during playback
                log("Click is disabled during playback")
                cv2.putText(frame, "Click is disabled during playback", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            else:
                mesh = markerfile_handler.get_mesh()
                marker_object = mesh.markers[frame_id_current]
                selected_marker_object = get_data_from_marker_id_selected(marker_object, marker_id_selected)
                
                if global_flag_onclick_left:
                    log("Left Click")
                    log(global_var_onclick_point)
                    selected_marker_object.x = global_var_onclick_point['x']
                    selected_marker_object.y = global_var_onclick_point['y']
                    selected_marker_object.status = CoordinateStatus.SET

                if global_flag_onclick_right:
                    log(f"Right Click")
                    log(global_var_onclick_point)
                    selected_marker_object.status = CoordinateStatus.NOT_ASSIGNED

                if global_flag_onclick_middle:
                    log(f"Middlet Click")
                    log(global_var_onclick_point)
                    selected_marker_object.status = CoordinateStatus.OFF_SCREEN

            global_flag_onclick_left = False
            global_flag_onclick_right = False
            global_flag_onclick_middle = False


        # Display the frame
        cv2.imshow(window_name, frame)

        # Wait for a key press, q to exit, space to start/stop the video (keep playing current frame)
        key = cv2.waitKey(1) & 0xFF
        if key in [ord('q'),ord('Q')]:
            # stop the autosave thread
            global_flag_autosave_enabled = False
            global_flag_autosave_calling = False

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
            marker_id_selected = key - ord('1')
            print(f"Selected Marker ID: {marker_id_selected} - {get_label_from_marker_id_selected(marker_id_selected)}")

        elif key == ord('o'):
            mesh = markerfile_handler.get_mesh()
            marker_object = mesh.markers[frame_id_current]
            selected_marker_object = get_data_from_marker_id_selected(marker_object, marker_id_selected)
            selected_marker_object.status = CoordinateStatus.OFF_SCREEN
        
        elif key == ord('p'):
            mesh = markerfile_handler.get_mesh()
            marker_object = mesh.markers[frame_id_current]
            selected_marker_object = get_data_from_marker_id_selected(marker_object, marker_id_selected)
            selected_marker_object.status = CoordinateStatus.NOT_ASSIGNED

        elif key == ord('a'):
            run_marker_regression(markerfile_handler, marker_id_selected, frame_id_current)

        elif key == ord('A'):
            run_marker_regression(markerfile_handler, marker_id_selected, frame_id_current, removeMode=True)

        elif key == ord('/'): # Seek to next SET point
            saved_frame = None
            flag_pause = False
            flag_is_set_marker_founded = False
            is_on_seeking = True

        elif key == ord("'"): # Jump to next SET point IMMEDIATELY
            log("Jumping to next SET point...")
            mesh = markerfile_handler.get_mesh()
            frame_id_current += 1
            while frame_id_current < mesh.frame_total-1:
                if is_set_marker_founded(markerfile_handler, marker_id_selected, frame_id_current):
                    break
                frame_id_current += 1
            print(f"Jumped to frame {frame_id_current}.")
            capture_handler.set(cv2.CAP_PROP_POS_FRAMES, frame_id_current)
            is_on_seeking = False
            flag_pause = True
            saved_frame = None

        elif key == ord(";"): # Jump to previous SET point IMMEDIATELY
            log("Jumping to previous SET point...")
            mesh = markerfile_handler.get_mesh()
            frame_id_current -= 1
            while frame_id_current > 0:
                if is_set_marker_founded(markerfile_handler, marker_id_selected, frame_id_current):
                    break
                frame_id_current -= 1
            print(f"Jumped to frame {frame_id_current}.")
            capture_handler.set(cv2.CAP_PROP_POS_FRAMES, frame_id_current)
            is_on_seeking = False
            flag_pause = True
            saved_frame = None

        elif key == ord('='):
            history_frame_render += 1
            print(f"History Frame Render: {history_frame_render}")
        
        elif key == ord('-'):
            history_frame_render -= 1
            if history_frame_render < 1:
                history_frame_render = 1
            print(f"History Frame Render: {history_frame_render}")