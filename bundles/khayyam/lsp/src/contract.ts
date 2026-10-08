// Reads the display contract, which is the single source of truth for what a role
// is and which scope names it. The server never invents a role name or a scope:
// both come from here, so a change to the contract reaches the editor through the
// server's legend without touching the server. The legend carries the role's NAME
// and nothing else, because a legend entry is the token TYPE the editor matches a
// styling rule against, whole: the editor reads the part of a RULE'S key before the
// first separator as that type and the part after it as a language, so a legend entry
// that carries a language of its own can never be matched by a rule keyed the same
// way, and the editor then discards the token while merging it into the grammar's.
// The language is stated where the editor asks for it instead — the `[khayyam]` block
// the colour rules sit in, and this server's provider document selector — and the
// role's TextMate scopes stay the grammar's business: a theme states a value for a
// scope, and a role is displayed through the token type the server answers in, which a
// client styles with a rule keyed by that type.
//
// Not every role has a TextMate scope. A role that declares itself `server-only` is
// one no scope can carry, because the whole of what distinguishes it is a block the
// grammar cannot see, and it says why in the contract. The server is the realization
// that can answer such a role, and it reaches a host as a token type like any other;
// `scopeFor` refuses to invent a scope for one, because a scope that names no
// position is a scope a theme would style for nothing.
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

export interface ContractRole {
  name: string;
  identity: string;
  appliesTo: string;
  /** The one thing a consumer must know before it can answer the role at all:
   *  `grammar-scope` (a scope carries it) or `server-only` (nothing a grammar
   *  emits can). See the contract's `conformance.howARoleIsImplemented`. */
  implementedBy: string;
  /** Required of a `server-only` role and of no other: why no scope can carry it. */
  serverOnlyBecause?: string;
  /** Absent for a `server-only` role, which has no scope to display through. */
  scopes?: string[];
  attributes: Record<string, string>;
}

export interface Contract {
  specification: string;
  version: string;
  roles: ContractRole[];
  attributeSchema: { attributes: Record<string, { required?: boolean }> };
}

const contractPath = join(dirname(fileURLToPath(import.meta.url)), "..", "..", "display", "display.json");

export const contract: Contract = JSON.parse(readFileSync(contractPath, "utf8"));

export const ROLES: readonly string[] = contract.roles.map((role) => role.name);

/** The scope a role is displayed through. A role with two scopes (comments) uses the
 *  first. A role declared server-only names none, and asking for one is refused by
 *  name rather than answered with `undefined`: the role is answered as a token type,
 *  and there is no TextMate scope standing behind it. */
export function scopeFor(role: string): string {
  const found = contract.roles.find((candidate) => candidate.name === role);
  if (!found) throw new Error(`role '${role}' is not in the display contract`);
  const scope = (found.scopes ?? [])[0];
  if (scope === undefined)
    throw new Error(
      `role '${role}' is declared server-only in the display contract, so it has no scope to display through: ` +
        (found.serverOnlyBecause ?? "the contract states no reason"),
    );
  return scope;
}

/** The legend the server advertises: one token type per role, in role order, each
 *  spelled exactly as the contract spells the role and carrying no language of its
 *  own. A legend entry is a token type, not a TextMate scope and not a selector:
 *  the editor matches a rule against the entry whole, and reads a separator inside a
 *  RULE'S key as the boundary between a type and a language. A name that welds the
 *  language to the role therefore has no rule that can match it (verified in the
 *  editor bundle: the token's type hierarchy is its own name, and the rule's type is
 *  the part before the separator), and an unmatched token is dropped while the
 *  grammar's tokens are merged in — the editor asks for the tokens, receives them,
 *  and draws nothing. A role's scope is the grammar's own business and reaches no
 *  client through this name: a client styles a role with a rule keyed by the role. */
export const LEGEND: string[] = [...ROLES];

/** Where a role sits in that legend, which is the token type the editor reads whole,
 *  or -1 when the contract names no such role: a role the editor cannot be told
 *  about is a token this server does not answer with. */
export function tokenTypeIndex(role: string): number {
  return ROLES.indexOf(role);
}
