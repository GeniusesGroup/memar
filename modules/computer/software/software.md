# Software

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### App kinds and run targets - edges/app.go
- **Idea**: app kinds Firmware, Hypervisor, Application, Game; run targets Local, Storage, Server, GUI, Edge.
- **Review questions**: are run targets a deployment projection rather than an app identity?

### App relations - edges/app-relation-app.go, app-relation-module.go, app-relation-object.go, app-relation-page.go, app-relation-widget.go
- **Idea**: SubCompile (a compact version such as GUI, Edge builds); OSImage / BinaryExecutable objects with TODO meta info about the image and application (framework, builder); empty placeholder files for module/page/widget relations.
- **Review questions**: is SubCompile a build-artifact relation or a deployment relation? Does the framework/builder metadata belong to a software bill-of-materials concept?

### Rule permission roles - edges/rule-relation-app.go
- **Idea**: roles over rules on an app: (Rule)Developer, (Rule)Observer, (Rule)Supervisor, (Rule)Executive (who administers the rule).
- **Review questions**: do these reuse the rights/delegate machinery instead of new labels?