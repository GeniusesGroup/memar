# Contribution
Follow hints or ask question from exiting contributors.

## Before contributing (design)
Read and understand [Memar](https://github.com/GeniusesGroup/memar) before making design judgments in this repository. This is a methodological filter, not a courtesy: Memar defines the way of thinking and modeling this project uses, and experience (three failed team-formation attempts) showed that contributors who start from industry defaults — common management vocabulary instead of extracted concepts — repeat exactly the failures the method exists to prevent. Candidates are asked to read Memar before interviews; if the model does not land, this project is not the right fit. See [README.md → Relationship to the wider Memar framework](README.md) and the vocabulary-discipline handoff in [`modules/management/vocabulary-discipline.handoff.md`](modules/management/vocabulary-discipline.handoff.md).

## Hints
- Suggest use hour for any domains that calculate data from other domains. other duration like minute or day are not efficient enough.
- To respect our timings rules add `-utc_...` e.g. `-utc_hour` or any other time epoch e.g `unix_...` to end of any time based domains.
- Don't Break content semantic in content visualization!
