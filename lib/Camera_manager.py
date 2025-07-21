from lib.event_object import Event_object
from lib.Camera import Camera


class CameraManager(Event_object):
    _instance = None

    def __init__(self):
        super().__init__()
        if CameraManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.cameras = {}
            self.main_camera = None
            CameraManager._instance = self

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = CameraManager()
        return cls._instance

    def register_camera(self, name, camera: Camera, set_as_main=False) -> bool:
        """Register a camera with a given name and optionally set it as the main camera."""
        if name in self.cameras:
            raise ValueError(f"Camera with the name '{name}' is already registered.")

        self.cameras[name] = camera
        if set_as_main:
            self.main_camera = camera
        return True

    def get_camera_by_name(self, name) -> Camera:
        """Retrieve a camera by its name."""
        return self.cameras.get(name)

    def get_main_camera(self) -> Camera:
        """Retrieve the main camera."""
        return self.main_camera

    def set_main_camera(self, camera: Camera):
        """Set the main camera."""
        self.main_camera = camera

    def set_main_camera_by_name(self, name):
        """Set the main camera by its name."""
        camera = self.get_camera(name)
        if camera:
            self.set_main_camera(camera)
        else:
            print(f"No camera found with the name '{name}'")


# Example usage:

# # Initialize the CameraManager
# camera_manager = CameraManager.get_instance()

# # Create cameras
# camera1 = Camera(800, 600, (0, 0), 1600, 1200)
# camera2 = Camera(800, 600, (400, 300), 1600, 1200)

# # Register cameras with names and optionally set as main camera
# camera_manager.register_camera("main_camera", camera1, set_as_main=True)
# camera_manager.register_camera("secondary_camera", camera2)

# # Try to register a camera with a name that already exists
# success = camera_manager.register_camera("main_camera", camera2)
# if not success:
#     print("Failed to register the camera.")

# # Set the main camera by name
# camera_manager.set_main_camera_by_name("secondary_camera")

# # Retrieve a camera by name
# retrieved_camera = camera_manager.get_camera("main_camera")

# # Check which camera is the main camera
# main_camera = camera_manager.get_main_camera()
# print(f"The main camera is: {main_camera}")
