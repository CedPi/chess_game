from base.base_controller import BaseController
from view.report_view import (
    ActorsAlphaReportView,
    ActorsRankingReportView,
    TournamentPlayersAlphaReportView,
    TournamentPlayersRankingReportView,
    AllTournamentsReportView,
    TournamentRoundsReportView,
    TournamentMatchesReportView,
)
from model.player import Player
from model.tournament import Tournament


class ReportController(BaseController):
    def __init__(self, view):
        super().__init__(view)
        self.default_view = view

    def menu(self):
        while True:
            self.view.ask()
            self.__call_adquate_action__()
            if self.view.menu.value == "R":
                break
            self.view.next()

    def __call_adquate_action__(self):
        match self.view.menu.value:
            case "1":
                self.view = ActorsAlphaReportView()
                self.all_actors_alpha_order()
            case "2":
                self.view = ActorsRankingReportView()
                self.all_actors_ranking_order()
            case "3":
                self.view = TournamentPlayersAlphaReportView()
                self.tournament_players_alpha_order()
            case "4":
                self.view = TournamentPlayersRankingReportView()
                self.tournament_players_ranking_order()
            case "5":
                self.view = AllTournamentsReportView()
                self.all_tournaments()
            case "6":
                self.view = TournamentRoundsReportView()
                self.tournament_turns()
            case "7":
                self.view = TournamentMatchesReportView()
                self.tournament_matches()
        self.view = self.default_view

    def all_actors_alpha_order(self):
        player_list = Player.get_list_order_by_name()
        self.view.display(player_list)

    def all_actors_ranking_order(self):
        player_list = Player.get_list_order_by_rank()
        self.view.display(player_list)

    def tournament_players_alpha_order(self):
        tournament_list = Tournament.get_list()
        self.view.ask(tournament_list)
        player_list = self.view.requested_tournament.get_player_list_order_by_name()
        self.view.display(player_list)

    def tournament_players_ranking_order(self):
        tournament_list = Tournament.get_list()
        self.view.ask(tournament_list)
        player_list = self.view.requested_tournament.get_player_list_order_by_rank()
        self.view.display(player_list)

    def all_tournaments(self):
        tournament_list = Tournament.get_list()
        self.view.display(tournament_list)

    def tournament_turns(self):
        tournament_list = Tournament.get_list()
        self.view.ask(tournament_list)
        round_list = self.view.requested_tournament.get_round_list()
        self.view.display(round_list)

    def tournament_matches(self):
        match_list = []
        tournament_list = Tournament.get_list()
        self.view.ask(tournament_list)
        round_list = self.view.requested_tournament.get_round_list()
        for round_elt in round_list:
            for match in round_elt.get_match_list():
                player_1 = {"player": Player.get(match.results[0][0]), "score": match.get_p1_score()}
                player_2 = {"player": Player.get(match.results[1][0]), "score": match.get_p2_score()}
                match_list.append((player_1, player_2))
        self.view.display(match_list)
