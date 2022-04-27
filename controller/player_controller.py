from base.base_controller import BaseController
from view.player_view import AddPlayerView, EditRankPlayerView, SearchPlayerView
from model.player import Player


class PlayerController(BaseController):
    def __init__(self, view):
        super().__init__(view)
        self.default_view = view

    def menu(self):
        while True:
            self.view.ask()
            self.__call_adquate_action()
            if self.view.menu.value == "R":
                break
            self.view.next()

    def __call_adquate_action(self):
        match self.view.menu.value:
            case "1":
                self.view = AddPlayerView()
                self.add()
            case "2":
                self.view = EditRankPlayerView()
                self.edit_rank_search()
            case "3":
                self.view = SearchPlayerView()
                self.search()
        self.view = self.default_view

    def add(self):
        self.view.ask()
        data = self.view.form.get_data()
        player = Player(**data)
        self.view.confirm(player)
        if self.view.record.value == "O":
            player.save()
            self.view.display_recording_confirm()
        else:
            self.view.display_recording_cancel()

    def edit_rank_search(self):
        self.view.ask()
        data = self.view.form.get_data()
        player_list = Player.search(data["last_name"], data["first_name"], data["date_of_birth"])
        self.edit_rank_player_list_choice(player_list)

    def edit_rank_choice(self, player_list: list):
        self.edit_rank_player_list_choice(player_list)

    def edit_rank_player_list_choice(self, player_list: list):
        if len(player_list) > 0:
            self.view.ask_choice(player_list)
            player = self.view.requested_player
            self.view.ask_new_rank()
            player.rank = int(self.view.player_new_rank)
            player.update()
            self.view.display()
        else:
            self.view.no_player_found()

    def search(self):
        self.view.ask()
        data = self.view.form.get_data()
        player_list = Player.search(data["last_name"], data["first_name"], data["date_of_birth"])
        self.view.display(player_list)
