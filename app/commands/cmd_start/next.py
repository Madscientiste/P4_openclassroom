from app.commands.base import BaseCommand
from app.utilities import typings, errors
from app.models import other, database


class Command(BaseCommand):
    name = "next"
    usage = "next"
    description = "Go to the next round"

    def run(self, context: typings.Context, tournament: database.Tournament, args: list, state: database.State):
        if tournament.rounds == state.current_round + 1:
            return
            
        round = tournament.round_instances[state.current_round]

        # Can't go to the next round if the matches aren't completed
        if None in [x.winner for x in round.matches]:
            raise errors.GenericError("Can't go to the next round, some matches need to be completed first")

        if not round.end_date:
            round.end_round()

        state.current_round += 1
        state.save()