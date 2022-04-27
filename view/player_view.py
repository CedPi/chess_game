from abc import abstractmethod
from base.base_view import BaseView
from base.widgets import WidgetChoice, WidgetDate, WidgetInt, WidgetIntRange, WidgetText, WidgetMenu
from base.form import Form
from model.player import Player


class PlayerView(BaseView):
    @abstractmethod
    def __init__(self):
        pass

    def next(self):
        input("Appuyez sur Entrée pour continuer...")

    @abstractmethod
    def display(self, player_list: list):
        pass

    @abstractmethod
    def ask(self, player_list: list):
        pass


class MenuPlayerView(PlayerView):
    def __init__(self):
        self.menu = WidgetMenu(
            "\nQue souhaitez-vous faire?",
            "Vous devez choisir une option dans la liste",
            {
                "1": "Ajouter un joueur",
                "2": "Modifier le classement d'un joueur",
                "3": "Rechercher un joueur",
                "R": "Retour",
            },
        )

    def ask(self):
        self.menu.init()
        self.menu.display()

    def display(self):
        pass


class AddPlayerView(PlayerView):
    def __init__(self):
        self.form = None
        self.record = None
        self.__init_form()
        self.__init_record()

    def ask(self):
        self.form.display()

    def confirm(self, player: Player):
        print("\nLe joueur suivant va être enregistré:")
        print(
            f"{player.get_full_name()} ({player.sex}), " + f"né(e) le {player.date_of_birth}, classé(e) {player.rank}"
        )
        self.record.display()

    def display(self):
        pass

    def __init_form(self):
        self.form = Form(
            {
                "last_name": WidgetText("Nom: ", "Le nom ne doit contenir que des lettres"),
                "first_name": WidgetText("Prénom: ", "Le nom ne doit contenir que des lettres"),
                "date_of_birth": WidgetDate(
                    "Date naissance (jj/mm/aaaa): ",
                    "La date doit être au format (jj/mm/aaaa",
                ),
                "sex": WidgetChoice("Sexe (M ou F): ", "Le sexe doit être M ou F", ["M", "F"]),
                "rank": WidgetIntRange(
                    "Classement (0 si non classé): ",
                    "Le classement doit être > 0",
                    min=0,
                    max=1000000,
                ),
            },
            "\nEnregistrement d'un joueur",
        )

    def __init_record(self):
        self.record = WidgetChoice("\nConfirmer (O / N) ?  ", "Choix possibles : O ou N", ["O", "N"])

    def display_summary(self, player_list: list):
        print("\nLes joueurs suivant vont être enregistrés:")
        i = 1
        for player in player_list:
            print(f"Joueur {i}")
            print(
                f"\t{player['last_name']} {player['first_name']}, né(e) le {player['date_of_birth']}, "
                + f"{player['sex']}, classé(e) {player['rank']} -- id : {player['id']}"
            )
            i += 1

    def display_confirm_recording(self):
        pass

    def display_recording_confirm(self):
        print(">> SUCCES: enregistrement OK")

    def display_recording_cancel(self):
        print("Annulation de l'enregistrement")


class EditRankPlayerView(PlayerView):
    def __init__(self):
        self.form = SearchPlayerView().form
        self.requested_player = None
        self.player_new_rank = None

    def ask(self):
        self.form.display()

    def ask_choice(self, player_list: list):
        player_list_menu = {}
        player_list_object = {}
        i = 1
        for player in player_list:
            player_name = self.format(f"{player.last_name} {player.first_name}", ".")
            player_str = f"{player_name}Classement: {player.rank}"
            player_list_menu[str(i)] = player_str
            player_list_object[i] = player
            i += 1
        menu = WidgetMenu(
            "\nChoisissez le joueur dont vous souhaitez modifier la classement",
            "Vous devez choisir un élément dans la liste",
            player_list_menu,
        )
        menu.display()
        self.requested_player = player_list_object[int(menu.value)]

    def ask_new_rank(self):
        rank = WidgetInt(
            f"Saisir le nouv. classement pour {self.requested_player.last_name} {self.requested_player.first_name}: ",
            "Vous devez saisir un nombre entier > 0",
        )
        rank.display()
        self.player_new_rank = rank.value

    def display(self):
        print("La modification a bien été enregistrée")

    def no_player_found(self):
        print("Aucun joueur trouvé")


class SearchPlayerView(PlayerView):
    def __init__(self):
        self.form = Form(
            {
                "last_name": WidgetText("Nom du joueur: ", "Veuiller indiquer un nom", required=True),
                "first_name": WidgetText("Prénom du joueur: ", "Veuiller indiquer un prénom", required=False),
                "date_of_birth": WidgetDate(
                    "Date de naissance: ", "Veillez indiquer la date au format jj/mm/aaaa", required=False
                ),
            },
            "\nRecherche d'un joueur",
        )

    def ask(self):
        self.form.display()

    def display(self, player_list: list):
        print("--- Liste des joueurs correspondant à la recherche ---")
        if len(player_list) == 0:
            print("Aucun joueur ne correspond à la recherche.")
            return -1
        col_name = self.format("NOM", " ")
        col_birth = self.format("DATE NAISS.", " ")
        col_sex = self.format("SEXE", " ")
        col_rank = self.format("CLASSEMENT", " ")
        print(f"{col_name}{col_birth}{col_sex}{col_rank}")
        for player in player_list:
            player_name = self.format(f"{player.last_name} {player.first_name}", " ")
            player_birth = self.format(f"{player.date_of_birth}", " ")
            player_sex = self.format(f"{player.sex}", " ")
            player_rank = self.format(f"{player.rank}", " ")
            print(f"{player_name}{player_birth}{player_sex}{player_rank}")
