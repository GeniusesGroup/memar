# List

## Model

- `(label)-[:list]->(thing)`
- `(thing)-[:list_in]->(label)`

## Policies (rules)

- List or label assign use to assign a label to a thing to help organize, track, and find records quickly and easily.
- e.g. Find all `spam` texts, Find `query` texts, Find all `exam` forms, ...
- Labels CAN also get other labels to organize them too.
- e.g. `spam`, `query`, ... CAN get `text-type` to FIND them easily by this label.
- Some usage example:
- label (`Commodity` own by User(`Omid`)) `list` Product (abc)
- label (`Suggestion` own by User(`Omid`)) `list` Task (123456)
- `label` is base on `thing`, so all thing level edges MUST be in mind
- `label` CAN be any user generated for any purpose:::
- ["MyGuitarPlayList", "Omid", "Owner"]
- Read in this model: label(MyGuitarPlayList) belong to user(Omid)
- ["MyGuitarPlayList", "Persia", "belongs_to_org"]
- Read in this model: label(MyGuitarPlayList) born in in org(Persia)
