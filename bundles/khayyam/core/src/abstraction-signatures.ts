/* For license and copyright information please see the LEGAL file in the code repository */

import { parseUnit } from "./parse.ts";
import type { FileSystem, Refused } from "./frontend.ts";
import type { Declaration, Unit } from "./sr.ts";

type Resolution = { declaration: Declaration; unit: Unit } | { refusal: Refused };

export function checkAbstractionSignatures(unit: Unit, fileSystem: FileSystem): Refused | undefined {
  const sources = new Map<string, Unit>([[unit.path, unit]]);

  function resolve(from: Unit, name: string, active = new Set<string>()): Resolution {
    const key = from.path + "\0" + name;
    if (active.has(key)) return { refusal: { outcome: "refuse", reason: "unresolved-type-declaration" } };
    active.add(key);
    const local = from.declarations.find(d => d.name === name && d.form !== "tp-in" && d.form !== "vr-in");
    if (local) return { declaration: local, unit: from };
    const inclusion = from.declarations.find(d => d.name === name && d.form === "tp-in");
    if (!inclusion || inclusion.form !== "tp-in") {
      return { refusal: { outcome: "refuse", reason: "unbound-type-name" } };
    }
    let target = sources.get(inclusion.path);
    if (!target) {
      const text = fileSystem.read(inclusion.path);
      if (text === undefined) return { refusal: { outcome: "refuse", reason: "unresolved-import" } };
      const parsed = parseUnit(inclusion.path, text);
      if (!parsed.ok) return { refusal: { outcome: "refuse", reason: parsed.fault.reason, line: parsed.fault.line } };
      target = parsed.unit;
      sources.set(inclusion.path, target);
    }
    if (!target.declarations.some(d => d.name === name)) {
      return { refusal: { outcome: "refuse", reason: "name-not-declared" } };
    }
    return resolve(target, name, active);
  }

  for (const method of unit.declarations) {
    if (method.form !== "tp-mt") continue;
    const receiver = method.owner.find(p => p.name === "self") ?? method.owner[0];
    if (!receiver || receiver.type.includes(".")) continue;
    const owner = resolve(unit, receiver.type);
    if ("refusal" in owner) return owner.refusal;
    if (owner.declaration.form !== "tp-ab") continue;
    for (const param of [...method.influencing, ...method.influenced]) {
      if (param.type.includes(".")) continue;
      const value = resolve(unit, param.type);
      if ("refusal" in value) return value.refusal;
      if (value.declaration.form === "tp-cp") {
        return {
          outcome: "refuse",
          reason: "capsule-in-abstraction-signature",
          line: method.line,
          reference: {
            parameter: param.name,
            type: param.type,
            declarationPath: value.unit.path,
            declarationLine: value.declaration.line,
          },
        };
      }
    }
  }
  return undefined;
}
