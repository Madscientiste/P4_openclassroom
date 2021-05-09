# flake8: noqa
from copy import deepcopy

from app.models import database, other

from .base import BaseView


class View(BaseView):
    """Tournament View
    Can render anything related to the tournament
    """

    def render_match(self, match: other.Match):
        self.set_title(f"{match.player1.first_name} vs {match.player2.first_name}")

        self.add_body("CMD : Description")
        self.add_body("-----------------")
        self.add_body(f"- a : if {match.player1.first_name} has won")
        self.add_body(f"- b : if {match.player2.first_name} has won")
        self.add_body("- c : if its a TIE")
        self.add_body("- d : to go back")

        self.add_body(" ")
        self.render_view()

    def render_selected_tournament(self, tournament: database.Tournament, commands: list):
        self.set_title(tournament.name)
        blacklist = ["players", "round_instances", "state"]
        space = self.SCREEN_WIDTH // 2

        state = tournament.state

        for key, value in deepcopy(tournament).to_dict().items():
            if key in blacklist:
                continue

            self.add_body(f"-- {key} : {value}")

        self.add_body(" ")
        self.add_body(self.center_item(f"Round {state.current_round + 1}", char="-"))
        self.add_body(" ")

        self.add_body(f"{'[ID]'.ljust(space, ' ')}{'STATE'.rjust(space, ' ')}")

        matches = tournament.round_instances[state.current_round].matches
        for index, match in enumerate(matches):
            index += 1

            player1 = match.player1.first_name
            player2 = match.player2.first_name

            # Colorizing
            warn = lambda text: self.colorize("warning", text)
            info = lambda text: self.colorize("info", text)
            success = lambda text: self.colorize("success", text)
            neutral = lambda text: self.colorize("neutral", text)

            # right_side = f"{success('ONGOING')}"
            # left_side = f"{neutral(player1)} vs {player2}"
            # match_id = str(index).center(2, " ")

            # if match.winner:
            #     winner = match.winner
            #     right_side = f"{warn('WINNER') if type(winner) == dict else info('TIE')}"

            #     if winner == player1:
            #         left_side = f"{warn(player1)} vs {player2}"
            #     else:
            #         left_side = f"{player1} vs {warn(player2)}"

            # left_side = f"[{match_id}] --- {left_side}"

            # left_side = left_side.ljust(space + 9, " ")
            # right_side = right_side.rjust(space + 9, " ")

            # self.add_body(f"{left_side}{right_side}")

        for index, match in enumerate(matches):
            match: other.Match
            index += 1

            p1 = match.player1
            p2 = match.player2

            right_side = f"{p1.points} - {p2.points}".rjust(space, " ")

            if p1.points and p2.points == 0.5:
                right_side = self.colorize("warning", "DRAW!".rjust(space, " "))

            match_id = str(index).center(2, " ")
            left_side = f"[{match_id}] --> {p1.first_name} < VS > {p2.first_name}".ljust(space, " ")

            self.add_body(f"{left_side}{right_side}")

        self.add_body(" ")
        self.add_body(self.center_item("Available Commands", char="-"))
        self.add_body(" ")

        self.show_commands(commands)

        self.render_view()

    def render_single(self, tournament: database.Tournament, title: str, hint=False):
        self.set_title(title)
        self.show_tournament(tournament)

        if hint:
            self.add_body(" ")
            self.add_body(self.center_item("Note", "-"))
            self.add_body(" ")

            command = self.colorize("success", f"tournament start {tournament.id}")
            self.add_body(f"---> To run the tournament type: {command}")
            self.render_view()

        self.render_view()

    def render_multiples(self, tournaments: list[database.Tournament], title: str, sort_by="id"):
        self.set_title(title)

        for index, tournament in enumerate(tournaments):
            index += 1

            self.add_body(f"----> Tournament {index} of {len(tournaments)} <-".ljust(self.SCREEN_WIDTH, "-"))
            self.show_tournament(tournament)
            self.add_body(" ")

        self.render_view()

    def tournament_quit(self):
        self.set_title("Main Application")
        self.add_body(self.center_item("Tournament Mode has been closed"))
        self.set_footer("-------")
        self.render_view(wait=True)
