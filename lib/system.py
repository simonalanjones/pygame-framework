import importlib
import inspect
import os

from lib.display import Display
from lib.controller import Controller
from lib.state_machine import StateMachine
from lib.event_object import EventObject
from lib.collision_manager import CollisionManager
from lib.debug import DebugOverlay
from lib.controller_registry import ControllerRegistry
from classes.controllers.input_controller import InputController

class System(EventObject):

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = System()
        return cls._instance

    def __init__(self):
        super().__init__()

        self.debug_overlay = DebugOverlay.get_instance(800, 600)

        self.collision_manger = CollisionManager.get_instance()
        self.display = Display()
        self.is_paused = False
        self.is_debugging = False

        self.controllers: list = []
        self.load_controllers()

        self.registry = ControllerRegistry(self.controllers)

        self.state_machine = StateMachine(self.event_manager, self.registry)

        self.is_wiping = False
        self.wipe_x = 0
        self.wipe_speed = 32
        self.callback_manager.register_callback(
            "begin_wipe_animation", lambda: self.on_begin_wipe()
        )
        self.callback_manager.register_callback(
            "clear_wipe", lambda: self.on_clear_wipe()
        )

       # self.event_manager.add_listener("pause_pressed", self.on_pause_pressed)
       # self.event_manager.add_listener("debug_pressed", self.on_debug_pressed)

        #self.event_manager.debug_listeners()





    def on_debug_pressed(self, data):
        self.is_debugging = not self.is_debugging
        self.display.set_debugging(self.is_debugging)

    def on_pause_pressed(self, data):
        if self.is_paused:
            self.is_paused = False
        else:
            self.is_paused = True
        print(self.is_paused)

    def on_begin_wipe(self):
        print("starting wipe...")
        self.is_wiping = True

    def on_clear_wipe(self):
        print("clearing wipe..")
        self.is_wiping = False
        self.wipe_x = 0

    def update(self, events, dt):
        # run any collision autoruns
        self.collision_manger.run_autorun_groups()

        if not self.state_machine.has_valid_state():
            return

        # let the state run its logic
        self.state_machine.update(events)

        # 1) Update each controller
        for controller in self.state_machine.get_state_controllers():
            # InputController always runs; others only when not paused
            if isinstance(controller, InputController) or not self.is_paused:
                if hasattr(controller, "update"):
                    controller.update(events, dt)
                else:
                    print(f"update() missing on {controller!r}")

        # 2) Gather surfaces from controllers that render
        surfaces = []
        for controller in self.state_machine.get_state_controllers():
            if hasattr(controller, "get_surface"):
                surf = controller.get_surface()
                if surf is not None:
                    surfaces.append(surf)

        # 3) Wipe transition logic
        if self.is_wiping:
            if self.wipe_x <= 224 * 4:
                self.wipe_x += self.wipe_speed
            else:
                self.event_manager.notify("wipe_animation_complete")

        # 4) Finally draw
        ##self.display.setDebug(self.debug_overlay)
        self.display.update(surfaces, self.is_wiping, self.wipe_x)



    def get_controller(self, target_controller):
        _controller = next(
            (
                controller
                for controller in self.controllers
                if controller.__class__.__name__.replace("Controller", "")
                == target_controller
            ),
            None,
        )
        return _controller

    def load_controllers(self):
        self.controllers = []
        controllers_dir = os.path.join("classes", "controllers")

        for fn in os.listdir(controllers_dir):
            if not fn.endswith("_controller.py"):
                continue
            module_name = fn[:-3]
            module_path = f"classes.controllers.{module_name}"
            module = importlib.import_module(module_path)

            for _, cls in inspect.getmembers(module, inspect.isclass):
                if issubclass(cls, Controller) and cls is not Controller:
                    inst = cls()
                    if not hasattr(inst, "rendering_order"):
                        inst.rendering_order = 0
                    self.controllers.append(inst)

        # sort by any rendering_order defined
        self.controllers.sort(key=lambda controller: controller.rendering_order)

        # call game_ready hooks
        for c in self.controllers:
            if callable(getattr(c, "game_ready", None)):
                c.game_ready()
