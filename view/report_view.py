from abc import abstractmethod
from base.base_view import BaseView
from base.widgets import WidgetMenu


class ReportView(BaseView):
    INT_SPACING = 20
    STR_SPACING = " "
    DEFAULT_SPACING = STR_SPACING * INT_SPACING

    @abstractmethod
    def __init__(self):
        pass

    def next(self):
        input("Appuyez sur Entrée pour continuer...")

    def __player_list_template__(self, last_name, first_name, date_birth, sex, rank):
        last_name_spacing = self.STR_SPACING * (self.INT_SPACING - len(last_name))
        first_name_spacing = self.STR_SPACING * (self.INT_SPACING - len(first_name))
        print(
            f"{last_name}{last_name_spacing}"
            + f"{first_name}{first_name_spacing}"
            + f"{date_birth}{self.DEFAULT_SPACING}"
            + f"{sex}{self.DEFAULT_SPACING}{rank}"
        )

    @abstractmethod
    def display(self, player_list: list):
        for player in player_list:
            self.__player_list_template__(
                player.last_name,
                player.first_name,
                player.date_of_birth,
                player.sex,
                player.rank,
            )

    @abstractmethod
    def ask(self, tournament_list: list):
        i = 1
        tournament_list_object = {}
        tournament_list_menu = {}
        for tournament in tournament_list:
            tournament_list_object[str(i)] = tournament
            tournament_list_menu[str(i)] = f"{tournament.name} - {tournament.date} - {tournament.place}"
            i += 1
        menu = WidgetMenu(
            "\nAfficher les informations de quel tournoi?",
            "Vous devez choisir une option dans la liste",
            tournament_list_menu,
        )
        menu.display()
        self.requested_tournament = tournament_list_object[menu.value]


class MenuReportView(ReportView):
    def __init__(self):
        self.menu = WidgetMenu(
            "\nQuel rapport voulez-vous afficher?",
            "Vous devez choisir une option dans la liste",
            {
                "1": "Liste de tous les acteurs par ordre alphabétique",
                "2": "Liste de tous les acteurs par classement",
                "3": "Liste des joueurs d'un tournoi par ordre alphabétique",
                "4": "Liste des joueurs d'un tournoi par classement",
                "5": "Liste des tournois",
                "6": "Liste des tours d'un tournoi",
                "7": "Liste des matchs d'un tournoi",
                "R": "Retour",
            },
        )

    def ask(self):
        self.menu.init()
        self.menu.display()

    def display(self):
        pass


class ActorsAlphaReportView(ReportView):
    def __init__(self):
        pass

    def ask(self):
        pass

    def display(self, player_list: list):
        print("\n--- Affichage de tous les joueurs par ordre alphabétique ---")
        super().display(player_list)


class ActorsRankingReportView(ReportView):
    def __init__(self):
        pass

    def ask(self):
        pass

    def display(self, player_list: list):
        print("\n--- Affichage de tous les joueurs par classement ---")
        super().display(player_list)


class TournamentPlayersAlphaReportView(ReportView):
    def __init__(self):
        self.requested_tournament = None

    def ask(self, tournament_list: list):
        super().ask(tournament_list)

    def display(self, player_list):
        print(
            "\n--- Affichage de tous les joueurs par ordre alphabétique du tournoi "
            + f"{self.requested_tournament.name} du {self.requested_tournament.date} "
            + f"à {self.requested_tournament.place} ---"
        )
        super().display(player_list)


class TournamentPlayersRankingReportView(ReportView):
    def __init__(self):
        self.requested_tournament = None

    def ask(self, tournament_list: list):
        super().ask(tournament_list)

    def display(self, player_list: list):
        print(
            "\n--- Affichage de tous les joueurs par classement du tournoi "
            + f"{self.requested_tournament.name} du {self.requested_tournament.date} "
            + f"à {self.requested_tournament.place} ---"
        )
        super().display(player_list)


class AllTournamentsReportView(ReportView):
    def __init__(self):
        pass

    def ask(self):
        pass

    def display(self, tournament_list: list):
        print("\n--- Liste de tous les tournois ---")
        for tournament in tournament_list:
            name = self.format(tournament.name, space_str=" ", repeat=40)
            place = self.format(tournament.place)
            date = self.format(tournament.date, space_str=" ", repeat=20)
            rcount = self.format(f"{tournament.round_count} tours", space_str=" ", repeat=20)
            tcontrol = self.format(tournament.time_control, space_str=" ", repeat=20)
            description = self.format(tournament.description, space_str="")
            print(f"{name}{place}{date}{rcount}{tcontrol}{description}")


class TournamentRoundsReportView(ReportView):
    def __init__(self):
        self.requested_tournament = None

    def ask(self, tournament_list):
        super().ask(tournament_list)

    def display(self, round_list):
        state = "Terminé" if self.requested_tournament.finished else "En cours"
        print(
            "\n--- Liste des tours du tournoi "
            + f"{self.requested_tournament.name} du {self.requested_tournament.date} "
            + f"à {self.requested_tournament.place} ({state}) ---"
        )
        local_spacing = self.STR_SPACING * 10
        for round_elt in round_list:
            print(f"{round_elt.name}{local_spacing}{round_elt.start}{local_spacing}{round_elt.end}")


class TournamentMatchesReportView(ReportView):
    def __init__(self):
        self.requested_tournament = None

    def ask(self, tournament_list):
        super().ask(tournament_list)

    def display(self, match_list):
        state = "Terminé" if self.requested_tournament.finished else "En cours"
        print(
            "\n--- Liste des matchs du tournoi "
            + f"{self.requested_tournament.name} du {self.requested_tournament.date} "
            + f"à {self.requested_tournament.place} ({state}) ---"
        )
        for match in match_list:
            p1 = match[0]["player"]
            p1_score = match[0]["score"]
            p2 = match[1]["player"]
            p2_score = match[1]["score"]
            local_spacing = self.STR_SPACING * (self.INT_SPACING - len(p1.last_name))
            print(f"{local_spacing}{p1.last_name} {p1_score} : {p2_score} {p2.last_name}")
