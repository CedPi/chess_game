import os
from abc import ABC, abstractmethod, abstractstaticmethod, abstractclassmethod
from tinydb import TinyDB


class BaseModel(ABC):
    DB_path = "database"
    DB_file = "db.json"
    os.makedirs(DB_path, exist_ok=True)
    DB = TinyDB(DB_path + "/" + DB_file)

    @abstractmethod
    def serialize(self) -> dict:
        pass

    @abstractstaticmethod
    def unserialize():
        pass

    @abstractstaticmethod
    def unserialize_list():
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractclassmethod
    def save_bulk(serialized_object_list: list):
        pass

    @abstractclassmethod
    def get(id):
        pass

    @abstractclassmethod
    def get_list():
        pass
