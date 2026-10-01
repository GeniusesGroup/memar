// A Language Server for Khayyam, speaking LSP over stdio.
//
// It does one job: hold the open documents, re-analyse one on change, answer
// textDocument/semanticTokens/full with a display-contract role per token, answer
// textDocument/definition with the place a name is declared at, and say what it could
// not read. This file is the process that runs it — the wiring from the wire to the
// answers and back — and every concern behind it is in a file that names it.
import { handle } from "./handlers.ts";
import { serve } from "./transport.ts";

serve(handle);
