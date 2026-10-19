# Meeting

A task-shaped conversation with minutes and forms. Optional management capability: Task, Group, Calendar, and Form already exist without a dedicated meeting type. Home: `modules-plugable/management/meeting`.

`(task)-[:meeting]->(---)` is a loop-edge (classification of that task), under `edges-loop/meeting`. Location remains an ordinary edge to estate.
