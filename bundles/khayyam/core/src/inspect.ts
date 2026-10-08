import type { Unit } from "./sr.ts";

export function inspect(unit: Unit): string {
  return JSON.stringify(unit, null, 2);
}
