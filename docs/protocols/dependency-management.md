---
Title: "Dependency and Version Management"
Status: Draft
Start Date: 2026-09-06
ID: 496870
---

# Dependency and Version Management

## Abstract
This document records Memar's position on how a project built with Memar manages its dependencies: where dependency knowledge lives, how versions are selected and pinned, and which mechanisms the ecosystem's package managers added that Memar treats as unnecessary. The position in one sentence: **the version-control repository is the dependency mechanism** — dependencies are references into other repositories, pinned the way the version-control system itself pins state, addressed as local relative paths — and the separate package-manager layer (central registries, remote import paths, transitive resolution algorithms, manifest-lockfile pairs) is a mechanism Memar's default does not require.

## Introduction

### Motivation
The ecosystem's package managers — whatever their differences — share one architecture: dependencies are identified by *remote import paths* resolved at build time through a central-or-federated registry, versions selected by a resolution algorithm, and the result recorded in a manifest-plus-lockfile pair owned by the package manager rather than the version-control system. From the perspective of a framework meant to be built *from* other repositories rather than installed *into* one, this architecture carries the same costs every time it is examined:

- **Remote addressing breaks reproducibility and self-containment.** A project whose dependency statements are URLs requires the network, the registry, and the URL's continued validity for every build — including builds of a clone made years later. The version-control system already solved pinning (commits, tags, sub-references); the package manager re-solved it worse, with a second addressing scheme layered on top.
- **Transitive dependency management imports problems the project does not own.** Resolution algorithms exist to reconcile conflicts among dependencies-of-dependencies — but a dependency's internal dependency choices are not the consumer's problem to reconcile; they are the dependency's own encapsulation boundary. An ecosystem that surfaces transitive conflicts to every consumer makes every project partially responsible for code it never calls.
- **The tool/registry/library separation eroded.** A platform's build tool grew into a package manager grew into a de facto central registry, and "the standard library" became inseparable from "the standard toolchain's module system" — making it hard to use the libraries without adopting the whole apparatus.

### Methodology
The position was formed by arguing the repository-reference alternative against the package-manager default across its strongest counter-arguments (transitive pinning, fork workflows, download cost). Those counter-arguments are recorded below rather than dropped; where they remain genuinely open, they are listed as unresolved questions.

## Explanation

### Dependencies are repository references
A Memar project's dependencies are declared as references to other projects' repositories — the same references the version-control system natively understands (submodule-style pointers, or the equivalent in whatever VCS a project uses) — and are pinned to specific revisions. The declared reference is a *local relative path* within the project; the VCS binds it to an external repository and revision. Consequences:

- A clone of the project is self-describing: every dependency, at its pinned revision, is derivable from the repository history plus the declared references — no registry, no manifest format, no lockfile reconciliation.
- The addressing scheme is the VCS's own — one addressing scheme, one pinning mechanism, one history. The package-manager layer adds no capability the VCS lacks for this purpose; it adds indirection, a second vocabulary, and a second source of truth.
- Version selection is explicit: the consumer chooses the revision it consumes. There is no resolution algorithm to run and no minimal-version selection to audit, because there is nothing to resolve — the pin *is* the decision.

### The boundary of the consumer's concern
A dependency's internal dependency structure is the dependency's own business. The consumer pins the dependency it uses; what that dependency does internally is its encapsulated choice. This is stated as a rule because the package-manager architecture makes transitive structure the consumer's problem by design (conflict resolution across the full graph), and that design decision is a substantial part of the complexity package managers exist to manage — complexity that disappears when the graph stops at declared references.

### Semantic versioning is available, not mandatory
Version numbering conventions (semantic versioning among them) are useful communication tools between producers and consumers. They are not enforced by a mechanism, because enforcement requires the package-manager layer this document removes, and because a version number is a *claim by the producer* — the consumer's defense against a bad claim is the same defense it has against any bad code: review, pinning, and its own tests. An ecosystem habit of treating "semver-compliant" as a guarantee is treated here as what it is: reliance on someone else's labeling discipline.

### What this position does not claim
It does not claim downloading is solved by nothing: large dependency trees are a real cost, and VCS-level sharing (a local clone cache shared across projects) is the expected mitigation — the same mechanism the VCS uses for its own object storage. It does not claim submodules are flawless: their sharp edges (detached heads, nested pinning, update ergonomics) are real and are the price of using the VCS's own primitive rather than a purpose-built layer. The claim is that the price is lower and the mechanism is honest — the dependency state is *in* the repository, visible in its history, reviewable in its diffs.

Vendoring (a mainstream language's historical `vendor/` directory and the pre-package-manager state of the PHP ecosystem) is the industry's earlier answer to the same reproducibility need; large monorepos' one-version policies solve dependency selection by eliminating it — evidence that explicit pinning and graph resolution are alternatives rather than necessities.
