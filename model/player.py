from uuid import uuid4
from tinydb import Query
from base.base_model import BaseModel


class Player(BaseModel):
    table = BaseModel.DB.table("players")

    def __init__(self, last_name, first_name, date_of_birth, sex, rank):
        self.id = str(uuid4())
        self.last_name = last_name.capitalize()
        self.first_name = first_name.capitalize()
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.rank = rank
        self.score = 0.0

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "sex": self.sex,
            "rank": self.rank,
        }

    def unserialize(player_dict: dict) -> "Player":
        player = Player(
            player_dict["last_name"],
            player_dict["first_name"],
            player_dict["date_of_birth"],
            player_dict["sex"],
            player_dict["rank"],
        )
        player.id = player_dict["id"]
        return player

    def unserialize_list(player_list: list):
        object_list = []
        for player in player_list:
            object_list.append(Player.unserialize(player))
        return object_list

    def save(self):
        serialized_player = self.serialize()
        if Player.get(self.id):
            self.update()
        else:
            Player.table.insert(serialized_player)

    def save_bulk(player_list_serialized: list):
        Player.table.insert_multiple(player_list_serialized)

    def update(self):
        Player.table.update(self.serialize(), Query().id == self.id)

    def search(last_name: str, first_name: str, birth: str, serialized=False):
        query_fname = Query().first_name != ""
        query_dbirth = Query().date_of_birth != ""
        if first_name != "":
            query_fname = Query().first_name == first_name.capitalize()
        if birth != "":
            query_dbirth = Query().first_name == first_name.capitalize()
        res = Player.table.search((Query().last_name == last_name.capitalize()) & query_fname & query_dbirth)
        if serialized:
            return res
        return Player.unserialize_list(res)

    def get(id, serialized=False):
        res = Player.table.search(Query().id == id)
        if len(res) == 0:
            return False
        if serialized:
            return res[0]
        return Player.unserialize(res[0])

    def get_list():
        return Player.table.all()

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"

    @classmethod
    def get_list_order_by_name(cls, serialized=False):
        player_list = Player.get_list()
        player_list.sort(key=Player.__order_name)
        if serialized:
            return player_list
        return Player.unserialize_list(player_list)

    @classmethod
    def get_list_order_by_rank(cls, serialized=False):
        player_list = Player.get_list()
        player_list.sort(key=Player.__order_rank)
        if serialized:
            return player_list
        return Player.unserialize_list(player_list)

    @classmethod
    def __order_name(cls, obj):
        return obj["last_name"]

    @classmethod
    def __order_rank(cls, obj):
        return obj["rank"]
