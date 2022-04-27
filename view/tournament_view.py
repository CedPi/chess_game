from abc import abstractmethod
from datetime import datetime
from base.base_view import BaseView
from base.widgets import WidgetChoice, WidgetDate, WidgetInt, WidgetMenu, WidgetMultiChoices, WidgetAlphaNum
from base.form import Form
from model.tournament import Tournament


class TournamentView(BaseView):
    SEPARATOR = " "
    SEPARATOR_INT = 10

    @abstractmethod
    def __init__(self):
        pass

    def next(self):
        input("Appuyez sur Entrée pour continuer...")

    @abstractmethod
    def display(self, player_list: list):
        pass

    @abstractmethod
    def ask(self, tournament_list: list):
        pass


class CreateTournamentView(TournamentView):
    def __init__(self, all_players: list):
        super().__init__()
        self.form = None
        self.player_list_object = {}
        self.requested_players = []
        self.__init_form(all_players)

    def ask(self):
        print("\n--- Création d'un nouveau tournoi ---")
        self.form.display()
        for choice in self.form.elements["player_list"].value:
            self.requested_players.append(self.player_list_object[choice].id)

    def confirm_generated_round(self, round_nb):
        print(f"\n----- TOUR {round_nb} -----")

    def ask_start_round(self, round_nb) -> str:
        input(f"\nAppuyez sur Entrée pour démarrer le TOUR {round_nb}")
        now = datetime.now()
        date_now = now.strftime("%d/%m/%Y")
        time_now = now.strftime("%H:%M:%S")
        print(f"Le TOUR {round_nb} a démarré le {date_now} à {time_now}")
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def ask_stop_round(self, round_nb) -> str:
        input(f"\nAppuyez sur Entrée pour arrêter le TOUR {round_nb}")
        now = datetime.now()
        date_now = now.strftime("%d/%m/%Y")
        time_now = now.strftime("%H:%M:%S")
        print(f"Le TOUR {round_nb} s'est terminé le {date_now} à {time_now}")
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def ask_update_results(self, p1_name: str, p2_name: str) -> tuple:
        print(f"\n--- Mise à jour des scores du match : {p1_name} Vs {p2_name} ---")
        p1_score = WidgetChoice(f"\t- Score {p1_name}: ", "Le score ne peut être que 0 ou 0.5 ou 1", ["0", "0.5", "1"])
        p1_score.display()
        p2_score = WidgetChoice(f"\t- Score {p2_name}: ", "Le score ne peut être que 0 ou 0.5 ou 1", ["0", "0.5", "1"])
        p2_score.display()
        return (float(p1_score.value), float(p2_score.value))

    def ask_update_rank(self):
        choice = WidgetChoice(
            "\nSouhaitez-vous mettre à jour un classement (O/N) ? ", "Choix possibles : O ou N", ["O", "N"]
        )
        choice.display()
        return choice.value

    def display_next_matches(self, pair_list: list):
        print("\n--- Les prochains matchs opposeront ---")
        for pair in pair_list:
            info_p1 = self.format(f"{pair[0].get_full_name()} ({pair[0].score}/{pair[0].rank})")
            info_p2 = f"{pair[1].get_full_name()} ({pair[1].score}/{pair[1].rank})"
            print(f"{info_p1}à\t\t{info_p2}")

    def display(self, player_list, final: bool):
        if final:
            print("\n--- CLASSEMENT FINAL DU TOURNOI ---")
        else:
            print("\n--- Classement provisoire du tournoi ---")
        i = 1
        for p in player_list:
            player_name = self.format(f"{p.last_name} {p.first_name}", " ")
            player_score = self.format(f"{p.score}   pts", " ")
            player_rank = self.format(f"class.:   {p.rank}", "")
            print(f"\t{i} : {player_name}{player_score}{player_rank}")
            i += 1

    def __init_form(self, player_list: list):
        player_list_menu = {}
        i = 1
        for player in player_list:
            self.player_list_object[str(i)] = player
            player_list_menu[
                str(i)
            ] = f"{player.last_name} {player.first_name} - {player.date_of_birth} - {player.sex} - cl. {player.rank}"
            i += 1
        self.form = Form(
            {
                "name": WidgetAlphaNum("Nom du tournoi: ", "Vous devez entrer un nom"),
                "place": WidgetAlphaNum("Lieu du tournoi: ", "Vous devez entrer un lieu"),
                "date": WidgetDate(
                    "Date du tournoi (jj/mm/aaaa): ", "Vous devez entrer une date au format jj/mm/aaaa"
                ),
                "description": WidgetAlphaNum("Description du tournoi: ", "Vous devez entrer une description"),
                "round_count": WidgetInt(
                    f"Nombre de tours (defaut: {Tournament.DEFAULT_COUNT_NUMBER}): ",
                    "Vous devez entrer un nombre > 0",
                    required=True,
                ),
                "time_control": WidgetMenu(
                    "Contrôle du temps",
                    "Vous devez sélectionner un élément dans la liste",
                    Tournament.TIME_CONTROL,
                    "Votre choix: ",
                ),
                "player_list": WidgetMultiChoices(
                    "\nChoisissez les joueurs participant au tournoi parmi la liste ci-dessous", "", player_list_menu
                ),
            },
            "Veuillez indiquer les informations concernant le tournoi",
        )


class ResumeTournamentView(CreateTournamentView):
    def __init__(self):
        self.requested_tournament = None

    def ask_tournament_to_resume(self, pending_tournaments: list):
        i = 1
        tournament_list_object = {}
        tournament_list_menu = {}
        for tournament in pending_tournaments:
            tournament_list_object[str(i)] = tournament
            tournament_list_menu[str(i)] = f"{tournament.name} - {tournament.date} - {tournament.place}"
            i += 1
        tournament_list_menu["R"] = "Retour"
        tournament_list_object["R"] = "R"
        menu = WidgetMenu(
            "\nReprendre le déroulement de quel tournoi?",
            "Vous devez choisir une option dans la liste",
            tournament_list_menu,
        )
        menu.display()
        self.requested_tournament = tournament_list_object[menu.value]
