# Politics of Appearance — Finnish proof of concept

This is a deliberately small, English-language oTree 6 proof of concept for a
matched-identity visual factorial experiment set in Finland. It contains two municipal-election choices and no
practice round, consent page, background questionnaire, or party-belonging
module.

## What is randomized

Four fictional identities are grouped into two fixed pairs. Every identity has
three appearance variants (`v1`, `v2`, `v3`), whose substantive mapping is kept
in the stimulus manifest rather than exposed in the participant interface.
For every participant and identity, the application independently randomizes:

1. appearance: progressive-coded, neutral, or conservative-coded;
2. economic policy: left or right;
3. sociocultural policy: liberal or conservative.

It also randomizes left/right screen position and which one of the two
candidates is rated after each vote. An identity is never repeated within a
participant. The randomization plan is stored on the participant record and all
treatment assignments are included in oTree's data export and the custom
candidate-level export.

## Outcomes

The primary outcome is forced-choice vote. After each task, one randomly chosen
candidate is rated on trustworthiness, competence, credibility, authenticity,
political suitability, appearance-policy fit, perceived left-right ideology,
and vote probability.

## Run locally

From this directory:

```bash
otree devserver
```

Then open the demo session named `finland_appearance_poc`.

Automated validation:

```bash
otree test finland_appearance_poc
```

## Important research status

The photographs are newly generated, fictional proof-of-concept stimuli. They
have **not** been perceptually validated. They must not be used for substantive
data collection until independent Finnish pretesting establishes perceived
ideology and checks attractiveness, class/status, apparent age, realism,
gender expression, AI artifacts, and resemblance to real people. A production
study should preregister stimulus-selection rules, audit demographic balance,
and generate a larger identity sample.

The source triptychs are retained under
`_static/appearance_experiment/images/source_triptychs/`. The cropped images
served to participants are under
`_static/appearance_experiment/images/candidates/`. The full prompt set and
generation notes are in `STIMULUS_GENERATION.md`.
