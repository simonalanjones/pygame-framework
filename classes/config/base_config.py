import os

class BaseConfig:
    config_values = None

    @classmethod
    def get(cls, key):
        return cls.config_values.get(key)

    @classmethod
    def get_file_path(cls, key):
        base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        parent_directory = os.path.dirname(base_directory)
        file_path = os.path.join(parent_directory, key)
        return file_path
