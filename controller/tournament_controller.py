from itertools import combinations
from base.base_controller import BaseController
from base.base_model import BaseModel
from model.tournament import Tournament
from model.player import Player
from model.match import Match
from model.round import Round
from controller.player_controller import PlayerController
from view.player_view import EditRankPlayerView


class TournamentController(BaseController):
    def __init__(self, view):
        super().__init__(view)
        self.player_list = []
        self.match_list = []
        self.round_list = []
        self.pairs = []
        self.current_round_nb = 1

    def create_tournament(self):
        self.view.ask()
        name, place, date, description, round_count, time_control, player_list = self.view.form.get_data().values()
        if round_count == "" or int(round_count) < 1:
            round_count = Tournament.DEFAULT_COUNT_NUMBER
        round_count = int(round_count)
        time_control = Tournament.TIME_CONTROL[time_control]
        player_list_ids = self.view.requested_players
        tournament = Tournament(name, place, date, description, round_count, time_control, player_list_ids)
        tournament.save()
        self.player_list = self.create_complete_player_list(tournament)
        self.play_tournament(tournament)

    def resume_tournament(self, pending_tournaments: list):
        self.view.ask_tournament_to_resume(pending_tournaments)
        if self.view.requested_tournament != "R":
            tournament = self.view.requested_tournament
            self.player_list = self.create_complete_player_list(tournament)
            self.load_state(tournament)
            self.compute_totals()
            self.play_tournament(tournament)

    def play_tournament(self, tournament: Tournament):
        matches_per_round = self.get_matches_per_round()
        while self.current_round_nb <= tournament.round_count:
            self.player_list.sort(key=lambda p: (-p.score, p.rank))
            round = self.get_existing_round(tournament, self.current_round_nb)
            if round is not None:
                if round.finished:
                    self.current_round_nb += 1
                    continue
            else:
                round = self.create_round(tournament)
            self.round_list.append(round)

            self.view.confirm_generated_round(self.current_round_nb)
            self.view.display(self.player_list, final=False)

            if self.current_round_nb == 1:
                if len(round.match_list) != matches_per_round:
                    self.generate_matches_first_round(round)
            else:
                if len(round.match_list) != matches_per_round:
                    self.generate_matches_next_round(round)
                    pass

            pair_list = []
            for match_id in round.match_list:
                pair = self.get_players_from_match(match_id)
                pair_list.append(pair)
            self.view.display_next_matches(pair_list)
            self.manage_round_time(round)
            for match_id in round.match_list:
                match = self.search_item(self.match_list, match_id)
                if not match.is_finished():
                    self.update_results(match)
                    self.compute_totals()
            round.finished = self.is_round_finished(round, matches_per_round)
            round.update()
            self.ask_update_rank()
            self.current_round_nb += 1
        tournament.finished = self.is_tournament_finished(tournament)
        tournament.update()
        self.player_list.sort(key=lambda p: (-p.score, p.rank))
        self.view.display(self.player_list, final=True)

    def get_existing_round(self, tournament: Tournament, current_round: int) -> Round | None:
        index = current_round - 1
        if 0 <= index < len(tournament.round_list):
            round_id = tournament.round_list[index]
            round = self.search_item(self.round_list, round_id)
            return round
        return None

    def create_round(self, tournament: Tournament) -> Round:
        round = Round(f"TOUR {self.current_round_nb}")
        tournament.round_list.append(round.id)
        round.save()
        tournament.save()
        return round

    def generate_pairs(self) -> list:
        combis = self.get_possible_combinations()
        matches_per_round = int(len(self.player_list) / 2)
        pair_combis = list(combinations(combis, matches_per_round))
        for pc in pair_combis:
            picked_pairs = []
            selected_players = []
            for pair in pc:
                player1 = pair["player1"]
                player2 = pair["player2"]
                player_pair = (player1, player2)
                rev_player_pair = (player2, player1)
                if player_pair in self.pairs or rev_player_pair in self.pairs:
                    break
                if player1 in selected_players or player2 in selected_players:
                    break
                selected_players.append(player1)
                selected_players.append(player2)
                picked_pairs.append(player_pair)
            if len(picked_pairs) != matches_per_round:
                continue
            else:
                self.pairs += picked_pairs
                return picked_pairs

    def get_possible_combinations(self) -> list:
        self.player_list.sort(key=lambda p: (-p.score, p.rank))
        combis = []
        existing_pairs = []
        for player1 in self.player_list:
            for player2 in self.player_list:
                if player1 == player2:
                    continue
                pair = (player1, player2)
                rev_pair = (player2, player1)
                if pair in existing_pairs or rev_pair in existing_pairs:
                    continue
                combo = {
                    "names": f"{player1.get_full_name()} ({player1.rank}) - "
                    + f"{player2.get_full_name()} ({player2.rank})",
                    "player1": player1,
                    "player2": player2,
                    "p1_score": player1.score,
                    "p2_score": player2.score,
                    "p1_rank": player1.rank,
                    "p2_rank": player2.rank,
                    "rank_diff": abs(player1.rank - player2.rank),
                }
                existing_pairs.append(pair)
                combis.append(combo)
                combis.sort(key=lambda c: (-c["p1_score"], -c["p2_score"], c["p1_rank"], c["p2_rank"], c["rank_diff"]))
        return combis

    def load_state(self, tournament: Tournament):
        """Loads the state of a pending tournament.
        Updates lists (rounds, matches, pairs).
        Used for resuming tournament.

        Args:
            tournament (Tournament): The tournament to load
        """
        for round_id in tournament.round_list:
            round = Round.get(round_id)
            self.round_list.append(round)
            for match_id in round.match_list:
                match = Match.get(match_id)
                self.match_list.append(match)
                player1 = Player.get(match.get_p1_id())
                player2 = Player.get(match.get_p2_id())
                self.pairs.append((player1, player2))

    def compute_totals(self):
        """Updates temporary scores"""
        for player in self.player_list:
            player.score = 0.0
        for match in self.match_list:
            if not match.is_finished():
                continue
            p1_id = match.get_p1_id()
            p1 = self.search_item(self.player_list, p1_id)
            p1.score += match.get_p1_score()
            p2_id = match.get_p2_id()
            p2 = self.search_item(self.player_list, p2_id)
            p2.score += match.get_p2_score()

    def ask_update_rank(self):
        choice = "O"
        player_list_display = self.player_list[:]
        player_list_display.sort(key=lambda p: (p.last_name, p.first_name))
        while True:
            choice = self.view.ask_update_rank()
            if choice == "N":
                break
            else:
                view = EditRankPlayerView()
                controller = PlayerController(view)
                controller.edit_rank_choice(player_list_display)

    def manage_round_time(self, round: Round):
        if round.start == "":
            round.start = self.view.ask_start_round(self.current_round_nb)
            round.update()
        if round.end == "":
            round.end = self.view.ask_stop_round(self.current_round_nb)
            round.update()

    def get_matches_per_round(self) -> int:
        return int(len(self.player_list) / 2)

    def get_players_from_match(self, match_id: str) -> tuple:
        match = self.search_item(self.match_list, match_id)
        p1 = self.search_item(self.player_list, match.get_p1_id())
        p2 = self.search_item(self.player_list, match.get_p2_id())
        return (p1, p2)

    def generate_matches_first_round(self, round: Round):
        """Creates matches then add them to the round.
        This is used for first round only, since pairing rules are differents.

        Args:
            round (Round): The round matches are added
        """
        i = 0
        pairs = []
        matches = []
        round.match_list.clear()
        matches_per_round = self.get_matches_per_round()
        while i < matches_per_round:
            match = Match(self.player_list[i].id, self.player_list[i + matches_per_round].id)
            matches.append(match)
            pairs.append((self.player_list[i], self.player_list[i + matches_per_round]))
            i += 1
        if len(matches) == matches_per_round:
            round.match_list = [m.id for m in matches]
            self.match_list += matches
            self.pairs += pairs
            [m.save() for m in matches]
            round.update()
        else:
            self.generate_matches_first_round(round)

    def generate_matches_next_round(self, round: Round):
        """Creates matches then add them to the round.
        This is used for all rounds except the fist one.

        Args:
            round (Round): The round matches are added
        """
        pairs = self.generate_pairs()
        for pair in pairs:
            match = Match(pair[0].id, pair[1].id)
            match.save()
            self.match_list.append(match)
            round.match_list.append(match.id)
        round.update()

    def update_results(self, match: Match):
        p1 = self.search_item(self.player_list, match.get_p1_id())
        p2 = self.search_item(self.player_list, match.get_p2_id())
        results = self.view.ask_update_results(f"{p1.get_full_name()}", f"{p2.get_full_name()}")
        match.update_results(results)
        match.update()
        self.compute_totals()

    def is_round_finished(self, round: Round, matches_per_round: int) -> bool:
        """Checks if round is finished based on the score of its matches
        and the number of matches per round.

        Args:
            round (Round): The round to check
            matches_per_round (int): Number of matches in round

        Returns:
            bool: The round finished (True) or not (False)
        """
        if len(round.match_list) == matches_per_round and round.start != "" and round.end != "":
            for match_id in round.match_list:
                match_obj = self.search_item(self.match_list, match_id)
                if not match_obj.is_finished():
                    return False
        else:
            return False
        return True

    def is_tournament_finished(self, tournament: Tournament) -> bool:
        """Checks if tournament is finished based on the status of its rounds

        Args:
            tournament (Tournament): The tournament to check

        Returns:
            bool: The tournament finished (True) or not (False)
        """
        if len(tournament.round_list) == tournament.round_count:
            for round_id in tournament.round_list:
                round_obj = self.search_item(self.round_list, round_id)
                if not round_obj.finished:
                    return False
        else:
            return False
        return True

    def create_complete_player_list(self, tournament: Tournament) -> list:
        """Creates a list of Player objects.
        Tounament objects only contain a list of player ids by default

        Args:
            tournament (Tournament): The tournament from which the list is created

        Returns:
            list: A list of Player instances
        """
        player_temp_list = []
        for player_id in tournament.player_list:
            player = Player.get(player_id)
            player_temp_list.append(player)
        return player_temp_list

    def search_item(self, search_list: list, id: str) -> BaseModel | None:
        if len(search_list) > 0:
            return [item for item in search_list if item.id == id][0]
        return None
