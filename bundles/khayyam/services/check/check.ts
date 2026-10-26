/* For license and copyright information please see the LEGAL file in the code repository */

// The command an agent runs to check Khayyam files with the core front end:
// `node check.ts --root DIR [--draft REPO_PATH=LOCAL_FILE ...] FILE...`
//
// FILE is a path inside DIR; a draft stands at the repository path it proposes, so a file
// written elsewhere is checked as if it were already there. One line per file, `accept` or
// `refuse` with the reason and line; exit 0 when all are accepted, 1 when any is refused,
// 2 when the command line is wrong. Nothing is read from the folder the run starts in.

import { checkFiles, parseCheckArguments } from "./check-files.ts";

const parsed = parseCheckArguments(process.argv.slice(2));
if (!parsed.ok) {
  console.error(`check: ${parsed.message}`);
  console.error("usage: node check.ts --root DIR [--draft REPO_PATH=LOCAL_FILE ...] FILE...");
  process.exitCode = 2;
} else {
  const result = checkFiles(parsed.value);
  for (const line of result.lines) console.log(line);
  process.exitCode = result.refused ? 1 : 0;
}
