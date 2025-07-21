from lib.event_object import Event_object
from lib.Viewport import Viewport


class ViewportManager(Event_object):
    _instance = None

    def __init__(self):
        super().__init__()
        self.viewports = {}
        self.primary_viewport = None  # Initialize the primary viewport

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ViewportManager()
        return cls._instance

    @classmethod
    def debug_viewports(cls):
        instance = cls.get_instance()  # Ensure we get the singleton instance
        print("Registered Viewports:")
        for name in instance.viewports.keys():
            print(name)
        if instance.primary_viewport:
            print(f"Primary Viewport: {instance.primary_viewport}")

    def count_viewports(self) -> int:
        """Count the number of registered viewports."""
        return len(self.viewports)

    def register_viewport(self, name, viewport: Viewport, set_as_primary=False) -> bool:
        """Register a viewport with a given name and optionally set it as the primary viewport."""
        if name in self.viewports:
            raise ValueError(f"Viewport with the name '{name}' is already registered.")

        self.viewports[name] = viewport
        if set_as_primary:
            self.primary_viewport = viewport

        # Debugging information
        self.debug_viewports()
        return True

    def get_viewport_by_name(self, name) -> Viewport:
        """Retrieve a viewport by its name."""
        return self.viewports.get(name)

    def get_primary_viewport(self) -> Viewport:
        """Retrieve the primary viewport."""
        return self.primary_viewport

    def set_primary_viewport(self, name) -> bool:
        """Set a viewport as the primary viewport by its name."""
        viewport = self.get_viewport_by_name(name)
        if viewport is None:
            print(f"No viewport found with the name '{name}'")
            return False

        self.primary_viewport = viewport
        return True

    def debug_sprites_in_viewport(self, name=None):
        """Debug all sprites in a particular viewport by name or the primary viewport if no name is provided."""
        viewport = (
            self.get_primary_viewport()
            if name is None
            else self.get_viewport_by_name(name)
        )
        if viewport is None:
            print(
                f"No viewport found with the name '{name}'"
                if name
                else "No primary viewport set"
            )
            return

        print(f"Sprites in viewport '{name if name else 'primary'}':")
        for sprite in viewport.sprites:
            print(sprite)

        print(
            f"Total number of sprites in viewport '{name if name else 'primary'}': {len(viewport.sprites)}"
        )


# from lib.Event_object import Event_object
# from lib.Viewport import Viewport

# #
# class ViewportManager(Event_object):
#     _instance = None

#     def __init__(self):
#         super().__init__()
#         self.viewports = {}

#     @classmethod
#     def get_instance(cls):
#         if cls._instance is None:
#             cls._instance = ViewportManager()
#         return cls._instance

#     @classmethod
#     def debug_viewports(cls):
#         instance = cls.get_instance()  # Ensure we get the singleton instance
#         print("Registered Viewports:")
#         for name in instance.viewports.keys():
#             print(name)

#     def count_viewports(self) -> int:
#         """Count the number of registered viewports."""
#         return len(self.viewports)

#     def register_viewport(self, name, viewport: Viewport) -> bool:
#         """Register a viewport with a given name"""
#         if name in self.viewports:
#             raise ValueError(f"Viewport with the name '{name}' is already registered.")

#         self.viewports[name] = viewport
#         # print("size of vps", self.count_viewports())
#         self.debug_viewports()
#         return True

#     def get_viewport_by_name(self, name) -> Viewport:
#         """Retrieve a viewport by its name."""
#         return self.viewports.get(name)

#     def debug_sprites_in_viewport(self, name):
#         """Debug all sprites in a particular viewport by name."""
#         viewport = self.get_viewport_by_name(name)
#         if viewport is None:
#             print(f"No viewport found with the name '{name}'")
#             return

#         print(f"Sprites in viewport '{name}':")
#         for sprite in viewport.sprites:
#             print(sprite)

#         print(f"Total number of sprites in viewport '{name}': {len(viewport.sprites)}")
