from base.base_controller import BaseController
from controller.player_controller import PlayerController
from controller.report_controller import ReportController
from controller.tournament_controller import TournamentController
from view.main_view import MainView
from view.player_view import MenuPlayerView
from view.report_view import MenuReportView
from view.tournament_view import CreateTournamentView, ResumeTournamentView
from model.player import Player


class MainController(BaseController):
    def __init__(self, view: MainView):
        super().__init__(view)

    def start(self, pending_tournaments: list):
        self.view.display_welcome()
        self.view.display_main_menu()
        self.__call_adequate_controller(pending_tournaments)

    def __call_adequate_controller(self, pending_tournaments: list):
        match self.view.main_menu.value:
            case "1":
                view = CreateTournamentView(Player.get_list_order_by_name())
                controller = TournamentController(view)
                controller.create_tournament()
            case "2":
                view = ResumeTournamentView()
                controller = TournamentController(view)
                controller.resume_tournament(pending_tournaments)
            case "3":
                view = MenuReportView()
                controller = ReportController(view)
                controller.menu()
            case "4":
                view = MenuPlayerView()
                controller = PlayerController(view)
                controller.menu()
            case "Q":
                pass
