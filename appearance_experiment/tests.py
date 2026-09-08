from otree.api import Bot, Submission

from . import pages
from .models import C


class PlayerBot(Bot):
    def play_round(self):
        yield Submission(
            pages.Task,
            dict(choice_side='left', decision_seconds=3.5),
            check_html=False,
        )
        yield Submission(
            pages.Evaluation,
            dict(
                trustworthiness=4,
                competence=4,
                credibility=4,
                authenticity=4,
                political_suitability=4,
                appearance_policy_fit=4,
                perceived_ideology=5,
                vote_probability=50,
            ),
            check_html=False,
        )
        if self.round_number == C.NUM_ROUNDS:
            yield Submission(pages.Completion, {}, check_html=False)
