# Criterion
e.g. [Thing(123), `get_criterion_by`, User(omid)]
e.g. [Staff(456), `get_criterion_by(score)`, User(AI)]

## Model
- `(thing)-[:get_criterion_by]->(user)`

## Fields
- `Criterion_Type` (`Field_Criterion_Type`) — the classification a criterion record carries. The source held a closed list: `Unset`, `Progress`, `Probability_Win`, `Probability_Failure`, `StoryPoint`, `Risk`. `StoryPoint` cites Agile/Scrum; the `Risk` member carried an unfinished note asking whether a risk rate is calculated data or something else.
- `Criterion_Point` (`Field_Criterion_Point`) — the measurement a criterion records. Story points are units of measure for expressing the effort a backlog item needs; teams assign them relative to work complexity, amount of work, and risk or uncertainty (<https://www.atlassian.com/agile/project-management/estimation>). The unit is deliberately undecided: the source says the value "can be any data e.g. percent, star, ...".
