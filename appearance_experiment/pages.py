from otree.api import Page

from .models import C, Player, candidate_payload, ensure_assignment


class Task(Page):
    form_model = 'player'
    form_fields = ['choice_side', 'decision_seconds']

    def vars_for_template(self):
        ensure_assignment(self.player)
        return dict(
            task_number=self.round_number,
            total_tasks=C.NUM_ROUNDS,
            left_candidate=candidate_payload(self.player, 'left'),
            right_candidate=candidate_payload(self.player, 'right'),
        )

    def before_next_page(self):
        if self.player.choice_side == 'left':
            self.player.choice_identity = self.player.left_identity
        else:
            self.player.choice_identity = self.player.right_identity


class Evaluation(Page):
    form_model = 'player'
    form_fields = [
        'trustworthiness',
        'competence',
        'credibility',
        'authenticity',
        'political_suitability',
        'appearance_policy_fit',
        'perceived_ideology',
        'vote_probability',
    ]

    def vars_for_template(self):
        ensure_assignment(self.player)
        target = candidate_payload(self.player, self.player.rating_target_side)
        return dict(
            task_number=self.round_number,
            total_tasks=C.NUM_ROUNDS,
            target=target,
        )


class Completion(Page):
    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS


page_sequence = [Task, Evaluation, Completion]
