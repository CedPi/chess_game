import os
from base.base_view import BaseView
from base.widgets import WidgetMenu


class MainView(BaseView):
    def __init__(self, nb_pending_tournaments: int):
        self.main_menu = WidgetMenu(
            "\n* Menu principal *",
            "Vous devez choisir un élément dans la liste.",
            {
                "1": "Créer un tournoi",
                "2": f"Reprendre un tournoi en suspens ( {nb_pending_tournaments} )",
                "3": "Afficher un rapport",
                "4": "Gérer les joueurs",
                "Q": "Quitter",
            },
        )

    def display_welcome(self):
        os.system("clear")
        print("\nBIENVENUE DANS LE PROGRAMME DE GESTION DE TOURNOIS D'ECHECS\n")
        print("(Appuyez sur Ctrl + C à tout moment pour interrompre le programme)\n")

    def display_main_menu(self):
        self.main_menu.display()

    def display_error(self):
        print("ERREUR: Réponse non valide")
