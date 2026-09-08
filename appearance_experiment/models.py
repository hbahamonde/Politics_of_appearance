from otree.api import *
import random


doc = """
Two-task Finnish matched-identity visual factorial proof of concept.

Four fictional candidate identities are divided into two fixed pairs. Each
identity has progressive-coded, neutral, and conservative-coded appearance
variants. Appearance, economic policy, and sociocultural policy are assigned
independently. Candidate side and the candidate evaluated after each choice are
also randomized.
"""


class C(BaseConstants):
    NAME_IN_URL = 'political-appearance-finland'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2

    IDENTITY_PAIRS = {
        1: ['01', '02'],
        2: ['03', '04'],
    }

    STYLE_CODES = ['v1', 'v2', 'v3']
    STYLE_LABELS = {
        'v1': 'progressive',
        'v2': 'neutral',
        'v3': 'conservative',
    }

    ECONOMIC_POSITIONS = {
        'left': (
            'The municipality should strengthen public services, even if '
            'this requires slightly higher taxation.'
        ),
        'right': (
            'The municipality should keep taxes low and make greater use '
            'of private service providers.'
        ),
    }

    CULTURAL_POSITIONS = {
        'liberal': (
            'The municipality should actively promote diversity and the '
            'equal treatment of minorities.'
        ),
        'conservative': (
            'The municipality should protect local traditions and shared '
            'cultural values.'
        ),
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


LIKERT_7 = [[i, str(i)] for i in range(1, 8)]
IDEOLOGY_11 = [[i, str(i)] for i in range(0, 11)]


class Player(BasePlayer):
    left_identity = models.StringField()
    right_identity = models.StringField()
    left_style_code = models.StringField()
    right_style_code = models.StringField()
    left_style_label = models.StringField()
    right_style_label = models.StringField()
    left_economic_position = models.StringField()
    right_economic_position = models.StringField()
    left_cultural_position = models.StringField()
    right_cultural_position = models.StringField()
    left_image_path = models.StringField()
    right_image_path = models.StringField()

    rating_target_side = models.StringField()
    rating_target_identity = models.StringField()

    choice_side = models.StringField(
        choices=[['left', 'Candidate A'], ['right', 'Candidate B']],
        label='Which candidate would you vote for?',
    )
    choice_identity = models.StringField()
    decision_seconds = models.FloatField(blank=True)

    trustworthiness = models.IntegerField(
        choices=LIKERT_7,
        label='How trustworthy does the candidate appear?',
        widget=widgets.RadioSelectHorizontal,
    )
    competence = models.IntegerField(
        choices=LIKERT_7,
        label='How competent does the candidate appear?',
        widget=widgets.RadioSelectHorizontal,
    )
    credibility = models.IntegerField(
        choices=LIKERT_7,
        label='How credible does the candidate appear?',
        widget=widgets.RadioSelectHorizontal,
    )
    authenticity = models.IntegerField(
        choices=LIKERT_7,
        label='How authentic does the candidate appear?',
        widget=widgets.RadioSelectHorizontal,
    )
    political_suitability = models.IntegerField(
        choices=LIKERT_7,
        label='How suitable does the candidate seem for political office?',
        widget=widgets.RadioSelectHorizontal,
    )
    appearance_policy_fit = models.IntegerField(
        choices=LIKERT_7,
        label='How well do the candidate\'s appearance and policy positions fit together?',
        widget=widgets.RadioSelectHorizontal,
    )
    perceived_ideology = models.IntegerField(
        choices=IDEOLOGY_11,
        label='Where would you place the candidate on the left–right scale?',
        widget=widgets.RadioSelectHorizontal,
    )
    vote_probability = models.IntegerField(
        min=0,
        max=100,
        label='How likely would you be to vote for this candidate? (0–100)',
    )


def _candidate_assignment(rng, identity):
    style_code = rng.choice(C.STYLE_CODES)
    economic = rng.choice(list(C.ECONOMIC_POSITIONS))
    cultural = rng.choice(list(C.CULTURAL_POSITIONS))
    return dict(
        identity=identity,
        style_code=style_code,
        style_label=C.STYLE_LABELS[style_code],
        economic=economic,
        cultural=cultural,
        image_path=(
            'appearance_experiment/images/candidates/'
            f'candidate_{identity}_{style_code}.png'
        ),
    )


def _build_plan(player):
    participant = player.participant
    rng = random.Random(f'{player.session.code}:{participant.code}')
    plan = []

    for round_number in range(1, C.NUM_ROUNDS + 1):
        identities = list(C.IDENTITY_PAIRS[round_number])
        rng.shuffle(identities)
        plan.append(
            dict(
                left=_candidate_assignment(rng, identities[0]),
                right=_candidate_assignment(rng, identities[1]),
                rating_target_side=rng.choice(['left', 'right']),
            )
        )

    participant.vars['stimulus_plan'] = plan


def ensure_assignment(player):
    participant = player.participant
    plan = participant.vars.get('stimulus_plan')
    if not plan:
        _build_plan(player)
        plan = participant.vars['stimulus_plan']

    if not player.field_maybe_none('left_identity'):
        assignment = plan[player.round_number - 1]
        left = assignment['left']
        right = assignment['right']

        player.left_identity = left['identity']
        player.right_identity = right['identity']
        player.left_style_code = left['style_code']
        player.right_style_code = right['style_code']
        player.left_style_label = left['style_label']
        player.right_style_label = right['style_label']
        player.left_economic_position = left['economic']
        player.right_economic_position = right['economic']
        player.left_cultural_position = left['cultural']
        player.right_cultural_position = right['cultural']
        player.left_image_path = left['image_path']
        player.right_image_path = right['image_path']
        player.rating_target_side = assignment['rating_target_side']
        player.rating_target_identity = assignment[assignment['rating_target_side']]['identity']


def creating_session(subsession):
    for player in subsession.get_players():
        ensure_assignment(player)


def candidate_payload(player, side):
    identity = getattr(player, f'{side}_identity')
    economic = getattr(player, f'{side}_economic_position')
    cultural = getattr(player, f'{side}_cultural_position')
    return dict(
        side=side,
        option='A' if side == 'left' else 'B',
        identity=identity,
        image_path=getattr(player, f'{side}_image_path'),
        economic_text=C.ECONOMIC_POSITIONS[economic],
        cultural_text=C.CULTURAL_POSITIONS[cultural],
    )


def custom_export(players):
    yield [
        'participant_code', 'round_number',
        'left_identity', 'left_style', 'left_economic', 'left_cultural',
        'right_identity', 'right_style', 'right_economic', 'right_cultural',
        'choice_side', 'choice_identity', 'decision_seconds',
        'rating_target_side', 'rating_target_identity',
        'trustworthiness', 'competence', 'credibility', 'authenticity',
        'political_suitability', 'appearance_policy_fit',
        'perceived_ideology', 'vote_probability',
    ]

    for player in players:
        yield [
            player.participant.code, player.round_number,
            player.left_identity, player.left_style_label,
            player.left_economic_position, player.left_cultural_position,
            player.right_identity, player.right_style_label,
            player.right_economic_position, player.right_cultural_position,
            player.choice_side, player.choice_identity, player.decision_seconds,
            player.rating_target_side, player.rating_target_identity,
            player.trustworthiness, player.competence, player.credibility,
            player.authenticity, player.political_suitability,
            player.appearance_policy_fit, player.perceived_ideology,
            player.vote_probability,
        ]
