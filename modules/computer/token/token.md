# Token
Authentication or access token

## Session ID

In computer science, a [session identifier](https://en.wikipedia.org/wiki/Session_ID), session ID or session token is a piece of data that is used in network communications (often over HTTPS) to identify a session, a series of related message exchanges. Session identifiers become necessary in cases where the communications infrastructure uses a stateless protocol such as HTTP. For example, a buyer who visits a seller's website wants to collect a number of articles in a virtual shopping cart and then finalize the shopping by going to the site's checkout page. This typically involves an ongoing communication where several webpages are requested by the client and sent back to them by the server. In such a situation, it is vital to keep track of the current state of the shopper's cart, and a session ID is one way to achieve that goal.

## Cryptography

## Usage

These rules base on `computer/token` domain

## Idea backlog from service code comments

Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Account deactivation
- **Idea**: full user deletion is not realistic because of legal complexity, so instead the register service must warn the user about deactivation rather than promise deletion.
- **Review questions**: is the sign-up warning an identity/registration concern ([user](../../identity/user/user.md)) while this module only revokes credentials on deactivation? Does deactivate-vs-delete need a user status that token merely reacts to? Who owns the legal-retention policy — the rule domain or [rights](../../rights/rights.md)?
