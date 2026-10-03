# Criterion

e.g. [Task(123), `get_criterion_by`, User(omid)]
e.g. [Staff(456), `get_criterion_by(score)`, User(AI)]

## Model

- `(thing)-[:get_criterion_by]->(user)`

## Fields

- `Criterion_Type` (`Field_Criterion_Type`) — the classification a criterion record carries. The source held a closed list: `Unset`, `Progress`, `Probability_Win`, `Probability_Failure`, `StoryPoint`, `Risk`. `StoryPoint` cites Agile/Scrum; the `Risk` member carried an unfinished note asking whether a risk rate is calculated data or something else.
- `Criterion_Point` (`Field_Criterion_Point`) — the measurement a criterion records. Story points are units of measure for expressing the effort a backlog item needs; teams assign them relative to work complexity, amount of work, and risk or uncertainty (<https://www.atlassian.com/agile/project-management/estimation>). The unit is deliberately undecided: the source says the value "can be any data e.g. percent, star, ...".

## Open questions

- **Is one word doing too much?** `Criterion_Point` names a magnitude whose unit is not fixed, which is the same defect the estate handoff names as the metric-choice principle: a word naming several quantities is a badly defined concept, and a rule on an ambiguous metric misleads regardless of execution. Whether `Criterion_Point` is a magnitude with a declared unit per criterion type, or a tagged value carrying its own unit, is undecided.
- **What does `Risk` measure?** The source's own unfinished note ("risk rate is calculated data or ... ?") is still open.
