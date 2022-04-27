import os
from view.main_view import MainView
from controller.main_controller import MainController
from base.widgets import WidgetChoice
from model.tournament import Tournament


class Main:
    def run(self):
        # p = Player.get("47565f2d-b5ae-47a2-8dea-bdfaaa21e692")
        # p.first_name = "Jerry"
        # p.save()
        menu = WidgetChoice(
            "\nQuitter le programme?\n[M]enu - [Q]uitter : ",
            "Choix possibles : M ou Q",
            ["M", "Q"],
        )

        while True:
            pending_tournaments = Tournament.get_pending_tournaments(serialized=False)
            if menu.value == "Q":
                break
            view = MainView(len(pending_tournaments))
            controller = MainController(view)
            controller.start(pending_tournaments)
            menu.init()
            menu.display()


if __name__ == "__main__":
    os.system("clear")
    try:
        Main().run()
    except KeyboardInterrupt:
        print("\nProgramme interrompu par l'utilisateur.\n\n")
    os.system("clear")
