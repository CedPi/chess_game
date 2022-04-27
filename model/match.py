import json
from uuid import uuid4
from tinydb import Query
from base.base_model import BaseModel


class Match(BaseModel):
    table = BaseModel.DB.table("matches")

    def __init__(self, p1_id, p2_id):
        self.id = str(uuid4())
        self.results = ([p1_id, -1], [p2_id, -1])

    def edit_score(self):
        self

    def serialize(self) -> dict:
        return {"id": self.id, "results": json.dumps(self.results)}

    def unserialize(match_dict: dict):
        results_data = json.loads(match_dict["results"])
        match = Match(results_data[0][0], results_data[1][0])
        match.results = ([results_data[0][0], results_data[0][1]], [results_data[1][0], results_data[1][1]])
        match.id = match_dict["id"]
        return match

    def unserialize_list():
        pass

    def save(self):
        serialized = self.serialize()
        if Match.get(self.id):
            self.update()
        else:
            Match.table.insert(serialized)

    def save_bulk(match_list_serialized: list):
        Match.table.insert_multiple(match_list_serialized)

    def update(self):
        Match.table.update(self.serialize(), Query().id == self.id)

    def load(self):
        pass

    def search():
        pass

    def get(id, serialized=False):
        res = Match.table.search(Query().id == id)
        if len(res) == 0:
            return None
        if serialized:
            return res[0]
        return Match.unserialize(res[0])

    def get_p1_id(self):
        return self.results[0][0]

    def get_p2_id(self):
        return self.results[1][0]

    def get_p1_score(self):
        return self.results[0][1]

    def get_p2_score(self):
        return self.results[1][1]

    def update_results(self, results):
        self.results[0][1] = results[0]
        self.results[1][1] = results[1]

    def is_finished(self):
        if self.get_p1_score() == -1 or self.get_p2_score() == -1:
            return False
        return True

    def get_list():
        pass
