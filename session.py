# mICE Project
# Session : Manage session files by ID

from utils import *

class CoordinateStatus(Enum):
    NOT_ASSIGNED = 0
    OFF_SCREEN = 1
    SET = 2
    ESTIMATED = 3

@dataclass
class Coordinate():
    status: CoordinateStatus = CoordinateStatus.NOT_ASSIGNED
    x: int = 0
    y: int = 0

DEFALUT_COORDINATE_FACTORY = lambda: Coordinate(CoordinateStatus.NOT_ASSIGNED, 0, 0)

@dataclass
class MeshReferencesDataclass():
    references_frame_id : int = 0
    point_origin : Coordinate = field(default_factory=DEFALUT_COORDINATE_FACTORY)
    axis_feeder : Coordinate = field(default_factory=DEFALUT_COORDINATE_FACTORY)
    axis_camera : Coordinate = field(default_factory=DEFALUT_COORDINATE_FACTORY)
    axis_upward : Coordinate = field(default_factory=DEFALUT_COORDINATE_FACTORY)
    warp_backgrid_5 : Coordinate = field(default_factory=DEFALUT_COORDINATE_FACTORY)
    warp_floorgrid_1 : Coordinate = field(default_factory=DEFALUT_COORDINATE_FACTORY)

@dataclass
class MeshMarkersDataclass():
    pellet : Coordinate = field(default_factory=DEFALUT_COORDINATE_FACTORY)
    nosetip : Coordinate = field(default_factory=DEFALUT_COORDINATE_FACTORY)
    finger_tip_right : Coordinate = field(default_factory=DEFALUT_COORDINATE_FACTORY)
    finger_thumb_right : Coordinate = field(default_factory=DEFALUT_COORDINATE_FACTORY)
    palm_right : Coordinate = field(default_factory=DEFALUT_COORDINATE_FACTORY)
    finger_tip_left : Coordinate = field(default_factory=DEFALUT_COORDINATE_FACTORY)

@dataclass
class Mesh():
    session_id : str = ""
    frame_total : int = 1

    references : list = field(init=False)
    markers : list = field(init=False)
    ts_last_updated : str = field(init=False)

    def __post_init__(self) -> None:
        self.references = [MeshReferencesDataclass()]
        self.markers = [MeshMarkersDataclass() for _ in range(self.frame_total)]
        self.ts_last_updated = get_timestamp()


class Markerfile():
    DEFAULT_CONFIG_SUPPORTED_VERSION = 1

    def __init__(self, session_id: str = "dummy", frame_total: int = 1, mesh: Mesh = None):
        self.__session_id = session_id
        self.__frames_total = frame_total
        if mesh is not None:
            self.__mesh = mesh
        else:
            self.init_mesh(self.__frames_total)

    def get_timestamp_lastupdated(self):
        return self.__mesh.ts_last_updated

    def is_version_supported(self, version: int):
        return version == self.DEFAULT_CONFIG_SUPPORTED_VERSION 
    
    def init_mesh(self, frame_total: int):
        self.__mesh = Mesh(self.__session_id, frame_total)

    def get_mesh(self):
        return self.__mesh
    
    def from_mesh(mesh: Mesh):
        markerfile = Markerfile(mesh.session_id, mesh.frame_total, mesh)
        return markerfile


class Session():

    DEFAULT_VIDEO_EXTENTION = ".MOV"        # Video file
    DEFAULT_MARKER_EXTENTION = ".marker"    # Pickle file

    def __init__(self, session_id: str):
        self.__session_id = session_id
        log(self.__session_id)

        self.set_videofile_dir()
        self.set_markerfile_dir()


    def get_default_session_dir(self):
        return os.path.join(os.getcwd(), 'dataset')
    

    def set_videofile_dir(self, path=None):
        if path:
            self.__video_dir = path
        else:
            self.__video_dir = self.get_default_session_dir()


    def get_videofile_dir(self):
        return self.__video_dir
    

    def get_videofile_path(self):
        return os.path.join(self.__video_dir, f"{self.__session_id}{self.DEFAULT_VIDEO_EXTENTION}")
    

    def is_videofile_founded(self):
        video_file_path = self.get_videofile_path()
        return os.path.exists(video_file_path)
    

    def set_markerfile_dir(self, path=None):
        if path:
            self.__marker_dir = path
        else:
            self.__marker_dir = self.get_default_session_dir()

    
    def get_markerfile_dir(self):
        return self.__marker_dir
    

    def get_markerfile_path(self):
        return os.path.join(self.__marker_dir, f"{self.__session_id}{self.DEFAULT_MARKER_EXTENTION}")
    

    def is_markerfile_founded(self):
        marker_file_path = self.get_markerfile_path()
        return os.path.exists(marker_file_path)
    

    def load_markerfile(self) -> Markerfile:
        marker_file_path = self.get_markerfile_path()
        if os.path.exists(marker_file_path):
            with open(marker_file_path, 'rb') as f:
                mesh = pickle.load(f)
                log(mesh.ts_last_updated)
                markefile_handler = Markerfile.from_mesh(mesh)
                return markefile_handler
        else:
            return None
        
    
    def save_markerfile(self, marker_object: Markerfile):
        marker_file_path = self.get_markerfile_path()
        with open(marker_file_path, 'wb') as f:
            pickle.dump(marker_object.get_mesh(), f)


    # not finished
    def set_config(self, config):
        self.__config = config
        print(f"Marker V.{self.__version}, Config V.{config['version']}")
        if self.__version == 0:
            print(f"Marker Initializing...")
            self.__version = config['version']
            # init
        elif self.__version == config['version']:
            print(f"Marker version matched.")
        else:
            print(f"Marker version not matched. Update required!")
            # Update
