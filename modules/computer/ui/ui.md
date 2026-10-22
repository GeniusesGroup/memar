---
Title: "GUI - Graphic User Interface"
Status: Draft
Start Date: 2021-05-25
ID: 450528
---

# GUI - Graphic User Interface

## Position on GUI Architecture
The dominant GUI toolkits and frameworks — desktop toolkits (Fyne, GTK, Qt, Flutter), web component libraries (React and its descendants), and the hybrid WebView wrappers — share one structural fault this protocol positions itself against: they are silent on architecture. Like [microservices](../../docs/modeling.md#domain-decomposition-over-aggregate-root-modeling) on the backend, they supply widgets and rendering while leaving every architectural question — application state, navigation, service access, validation placement — to each application's own improvisation. The result is the same everywhere: each application re-invents its own routing, its own state shape, and its own way of reaching the backend, and no two do it the same way.

Memar's position, stated as three separations, is inherited from the web standards' one genuinely proven idea: **content, presentation, and logic are three different concerns, expressed in three different, separately-evolvable artifacts.** The ecosystem's newer toolkits abandoned this separation — embedding layout, styling, and behavior in one mixed medium (a claim React's own JSX explicitly made: separation of *technologies* had failed, so separation of *concerns* was abandoned with it) — and then rebuilt each concern per-application as ad-hoc patterns.

From that position follow the specific stances this protocol carries:

- **Widget, not component.** A *widget* is a named, stateful element with application-wide identity: one instance exists, it acquires the data it needs when it needs it, and it participates in the application's own state model. A *component* is a rendering template instantiated per use, with per-instance state and data passed in from above — the unit the component frameworks standardized. Memar's GUI model is widget-based: per-instance anonymous components push application structure into data-passing conventions that bypass the state model entirely, which is precisely the layering-by-convention this protocol exists to prevent.
- **Page state and history are protocol concerns.** The browser's History API is built on the server-rendered-page assumption and accepts arbitrary state blobs with no structure — every application invents its own page-state shape on top. Memar's model (see [Page](#page) below) defines page identity and state as protocol-level structures, so navigation, deep-linking, and state restoration are uniform across applications instead of per-framework inventions.
- **One routing authority per application.** Activation of pages on URL change is not something each widget library may privately implement; in one application, one capability is performed in one place. A toolkit that brings its own router is fragmenting the application's architecture, not extending it.
- **The GUI does not speak the network.** No part of a Memar GUI communicates with a backend directly; it calls generated SDK functions for the services it needs (see [SDK](../process/service/sdk/sdk.md)). The GUI developer works against service abstractions — the generated code is the only thing that knows a network exists. This removes an entire class of application code (fetching, retry, serialization glue) from every GUI and keeps the service contract in exactly one place.
- **Validation is shared, not duplicated.** Validation logic belongs to the business-logic layer and is generated once for both the server and the GUI client (the accessor/setter pattern realizing it per field), so server and client validate identically instead of two hand-maintained rule sets drifting apart.

## Page

### ID
- To have canonical page IDs calculate it from hash of URN.
- ID is first 64bit of SHA3-256 hash of page URN!
- Zero ID means no page!

### URN
`urn:giti:{{domain-name}}:page:{{page-name}}`

## Resources
- https://developer.mozilla.org/en-US/docs/Web/API/Window
- https://github.com/gopherjs/gopherjs
- https://webvision.mozilla.org/full/
- https://extensiblewebmanifesto.org/
- https://open-ui.org/
- https://www.chromium.org/teams/web-capabilities-fugu/
- https://fugu-tracker.web.app/

## Related Projects
All below projects have many problems.
- [Flutter](https://docs.flutter.dev/) mix content(HTML) and style(CSS) in to logic(JS, Dart, Go, ...) language
- https://github.com/maxence-charriere/go-app/blob/master/pkg/ui/scroll.go		>> indicate scroll as a content not behavior of elements
- https://github.com/gioui/gio
- https://github.com/asticode/go-astilectron
- https://github.com/zserge/lorca
- https://github.com/wailsapp/wails
- https://github.com/sciter-sdk/go-sciter
