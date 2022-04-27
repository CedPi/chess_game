import json
from datetime import datetime
from uuid import uuid4
from tinydb import Query
from base.base_model import BaseModel
from model.match import Match


class Round(BaseModel):
    table = BaseModel.DB.table("rounds")

    def __init__(self, name: str):
        self.id = str(uuid4())
        self.start = ""
        self.end = ""
        self.name = name
        self.match_list = []
        self.finished = False

    def start(self):
        self.start = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def stop(self):
        self.end = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "start": self.start,
            "end": self.end,
            "name": self.name,
            "match_list": json.dumps(self.match_list),
            "finished": self.finished,
        }

    def unserialize(round_dict: dict):
        match_data = json.loads(round_dict["match_list"])
        round = Round(
            round_dict["name"],
        )
        round.id = round_dict["id"]
        round.match_list = list(match_data)
        round.start = round_dict["start"]
        round.end = round_dict["end"]
        round.finished = round_dict["finished"]
        return round

    def unserialize_list():
        pass

    def save(self):
        serialized = self.serialize()
        if Round.get(self.id):
            self.update()
        else:
            Round.table.insert(serialized)

    def save_bulk(round_list_serialized: list):
        Round.table.insert_multiple(round_list_serialized)

    def update(self):
        Round.table.update(self.serialize(), Query().id == self.id)

    def load(self):
        pass

    def search():
        pass

    def get(id, serialized=False):
        res = Round.table.search(Query().id == id)
        if len(res) == 0:
            return False
        if serialized:
            return res[0]
        return Round.unserialize(res[0])

    def get_match_list(self, serialized=False):
        return_list = []
        for match_id in self.match_list:
            return_list.append(Match.get(match_id, serialized))
        return return_list

    def get_list():
        pass
