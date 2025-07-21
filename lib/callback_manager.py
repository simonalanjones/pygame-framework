# lib/callback_manager.py

from typing import Callable, Any
from enum import Enum

class CallbackManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = CallbackManager()
        return cls._instance

    # Class-level dictionaries
    _callbacks: dict[Any, Callable[..., Any]] = {}
    _callback_names: dict[Any, str] = {}

    @classmethod
    def register_callback(cls, key: Any, callback: Callable[..., Any], name: str = None) -> None:
        cls._callbacks[key] = callback
        if name:
            cls._callback_names[key] = name

    @classmethod
    def get_callback(cls, key: Any) -> Callable[..., Any] | None:
        return cls._callbacks.get(key)

    @classmethod
    def callback_exists(cls, key: Any) -> bool:
        return key in cls._callbacks

    @classmethod
    def callback(cls, key: Any, *args, **kwargs) -> Any:
        callback_function = cls._callbacks.get(key)
        if callback_function is not None:
            return callback_function(*args, **kwargs)
        else:
            print(f"[CallbackManager] No callback found for key: {key}")
            return None

    @classmethod
    def debug_callbacks(cls) -> None:
        print("Registered Callbacks:")
        for key, callback in cls._callbacks.items():
            name = cls._callback_names.get(key, str(key))
            print(f"{name}: {callback.__name__ if hasattr(callback, '__name__') else callback}")

# class CallbackManager:
#     _instance = None
#
#     @classmethod
#     def get_instance(cls):
#         if cls._instance is None:
#             cls._instance = CallbackManager()
#         return cls._instance
#
#     # Class-level dictionary to store callbacks
#     callbacks = {}
#
#     # Class-level dictionary to store callback names (labels)
#     callback_names = {}
#
#     @classmethod
#     def register_callback(cls, key, callback, name=None):
#         cls.callbacks[key] = callback
#
#         # Store the callback name if provided
#         if name:
#             cls.callback_names[key] = name
#
#     @classmethod
#     def get_callback(cls, key):
#         return cls.callbacks.get(key, None)
#
#     @classmethod
#     def callback_exists(cls, key):
#         return key in cls.callbacks
#
#     def callback(cls, key, optional_param=None):
#         callback_function = cls.callbacks.get(key)
#         if callback_function is not None:
#             if optional_param is not None:
#                 return callback_function(optional_param)
#             else:
#                 return callback_function()
#         else:
#             # handle the case where the key is not found
#             print(f"No callback found for key: {key}")
#             return None
#
#     @classmethod
#     def debug_callbacks(cls):
#         print("Callbacks:")
#         for key, callback in cls.callbacks.items():
#             # Get the callback name from the dictionary, or use the key as a fallback
#             name = cls.callback_names.get(key, key)
#             print(
#                 f"{name}: {callback.__name__ if hasattr(callback, '__name__') else callback}"
#             )
