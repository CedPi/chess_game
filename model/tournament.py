import json

from uuid import uuid4
from tinydb import Query
from base.base_model import BaseModel
from model.player import Player
from model.round import Round


class Tournament(BaseModel):
    table = BaseModel.DB.table("tournaments")
    TIME_CONTROL = {"1": "bullet", "2": "blitz", "3": "coup rapide"}
    DEFAULT_COUNT_NUMBER = 4

    def __init__(self, name, place, date, description, round_count, time_control, player_list):
        self.id = str(uuid4())
        self.name = name
        self.place = place
        self.date = date
        self.description = description
        self.round_count = round_count
        self.time_control = time_control
        self.player_list = player_list
        self.round_list = []
        self.finished = False

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "place": self.place,
            "date": self.date,
            "description": self.description,
            "round_count": self.round_count,
            "time_control": self.time_control,
            "player_list": json.dumps(self.player_list),
            "round_list": json.dumps(self.round_list),
            "finished": self.finished,
        }

    def unserialize(tournament_dict: dict):
        player_data = json.loads(tournament_dict["player_list"])
        round_data = json.loads(tournament_dict["round_list"])
        tournament = Tournament(
            tournament_dict["name"],
            tournament_dict["place"],
            tournament_dict["date"],
            tournament_dict["description"],
            tournament_dict["round_count"],
            tournament_dict["time_control"],
            list(player_data),
        )
        tournament.id = tournament_dict["id"]
        tournament.round_list = list(round_data)
        tournament.finished = tournament_dict["finished"]
        return tournament

    def unserialize_list(tournament_list: list):
        object_list = []
        for tournament in tournament_list:
            object_list.append(Tournament.unserialize(tournament))
        return object_list

    def save(self):
        serialized = self.serialize()
        if Tournament.get(self.id):
            self.update()
        else:
            Tournament.table.insert(serialized)

    def save_bulk(tournament_list_serialized: list):
        Tournament.table.insert_multiple(tournament_list_serialized)

    def update(self):
        Tournament.table.update(self.serialize(), Query().id == self.id)

    def get(id, serialized=False):
        res = Tournament.table.search(Query().id == id)
        if len(res) == 0:
            return False
        if serialized:
            return res[0]
        return Tournament.unserialize(res[0])

    @classmethod
    def get_pending_tournaments(cls, serialized=False):
        res = Tournament.table.search(Query().finished == False)  # noqa: E712
        if serialized:
            return res
        return Tournament.unserialize_list(res)

    def get_list(serialized=False):
        res = Tournament.table.search(Query().id != "")
        if serialized:
            return res
        return Tournament.unserialize_list(res)

    def get_round_list(self, serialized=False):
        return_list = []
        for round_id in self.round_list:
            return_list.append(Round.get(round_id, serialized))
        return return_list

    def get_player_list_order_by_name(self, serialized=False):
        return_list = []
        for player_id in self.player_list:
            return_list.append(Player.get(player_id, serialized))
        return_list.sort(key=Tournament.__order_name)
        return return_list

    def get_player_list_order_by_rank(self, serialized=False):
        return_list = []
        for player_id in self.player_list:
            return_list.append(Player.get(player_id, serialized))
        return_list.sort(key=Tournament.__order_rank)
        return return_list

    @classmethod
    def __order_name(cls, player):
        return player.last_name

    @classmethod
    def __order_rank(cls, player):
        return player.rank
