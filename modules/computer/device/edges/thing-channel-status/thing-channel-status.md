# Thing channel status

## Model

- Candidate (unconfirmed): channel state labels `Off`, `Offline` on the thing-channel (iota flags `Status_Off` / `Status_Offline` in package `label`).

## Policies (rules)

- Source TODO (recorded twice): the status "can indicate in `thing-signal` subdomain as a state of a channel — e.g. off state need to change the led state on thing cover" (also phrased as IO subdomain).

## Placement

- **Core `device` keeps channel state for now; ownership between the channel and signal subdomains is open (create now, decide later).** Entry point is the channel, instantiated from device — filed here. The source's own `thing-signal`/IO TODO points at the existing siblings [signal-input](../signal-input/signal-input.md) and [signal-output](../signal-output/signal-output.md) inside this module, not at a new module: if the status only parameterizes channel behavior it stays (parameters vs semantics), and processing that drives physical indicators must stay with the capability that owns the channel (a pluggable must own its complete capability — never edge here, behavior elsewhere).

## Open questions

- Which domain owns channel state?
- Does the status drive physical indicators (LED on the thing cover)?

