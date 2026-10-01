/** Where an artifact stands, and how one artifact names another. The layout is
 *  fixed by the plan — artifacts are build products under the target's `build/`
 *  and are never a source of truth (execution.md → Compile cache) — and a URI is
 *  written from the repository root (the import-address rule), so an artifact
 *  keeps the URI's own path under the build root. A unit that is linked instead
 *  of compiled stands where its module stands, and the specifier between two
 *  artifacts is the same whether the second one is compiled or linked. */
export function artifactPath(buildRoot: string, uri: string): string {
  return `${buildRoot}/${uri.replace(/\.kh$/, ".js")}`;
}

export function directory(path: string): string {
  const at = path.lastIndexOf("/");
  return at < 0 ? "." : path.slice(0, at);
}

export function relativeSpecifier(fromDirectory: string, target: string): string {
  const from = fromDirectory.split("/").filter((part) => part !== "" && part !== ".");
  const to = target.split("/");
  let shared = 0;
  while (shared < from.length && shared < to.length && from[shared] === to[shared]) {
    shared += 1;
  }
  const up = from.length - shared;
  const joined = [...Array<string>(up).fill(".."), ...to.slice(shared)].join("/");
  return joined.startsWith(".") ? joined : `./${joined}`;
}
