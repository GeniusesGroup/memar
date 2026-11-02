---
Title: "Filesystem Rule — No File Concept Outside the Filesystem"
Labels: Draft
Start Date: 2026-10-31
---
# Filesystem Rule — No File Concept Outside the Filesystem
A rule of this repository, held for the [filesystem](../../filesystem.md). It applies wherever an abstraction, a service, a widget, an error or a document of a module other than the filesystem is written, in every language.

## The rule
- **Only the filesystem module names a file, a directory (a folder) or a path.** No other module declares one, embeds one, takes one as an argument, returns one, or states one in a name, a field, a method, an error or a text. The words `file`, `directory`, `folder`, `path` and their kin do not appear in another module's abstraction, whatever they would mean there.
- **A module names what the thing is** (a task, a document, a record, a place, a label, a project) and reaches it through the [memory port](../../../../../../modules/computer/memory/memory.md) and the [record contract](../../../store/record/record.md). That the thing is held today as a file is the realization of an adapter, never a part of the thing.
- **What must touch the operating system does it through the filesystem module's abstractions and services,** and a module that needs one the filesystem does not have records the gap as a task for the filesystem.
- **An import of the filesystem's abstraction by another module is a violation, not an exemption,** unless the importing module is a realization of the memory port. A module that needs "where it is" imports the record or the label, which the filesystem's adapter binds to a path.
- **Existing mentions are debts.** A module that names a file today is listed as a task to remove it; it does not receive new mentions while it waits.

## Why it exists
The owner's ruling (2026-10-31), at the review of the project module's abstraction, which named a folder, a top folder and a place as a path in a kernel module. A file is a storage artifact that leaked into the model ([Reevaluating the Filesystem](../../filesystem.md#storage-leakage-when-constraints-dictate-models)); naming it in a module's abstraction ties that module to the leak, and every later replacement of the files adapter would have to find and change each of them.

## Keep it or drop it
An organization whose system is bound to an operating system's files may name them in the module that uses them, and remain conformant to Memar's concepts, at the cost that each such module is re-written the day the files go.

## What this rule does not claim
- It does not claim the filesystem module is where files are good; the module's own stance is [the check](../../filesystem.practice.md) whether a system needs the filesystem at all.
- It does not forbid the word where it is the subject of text about the filesystem itself, such as a document that critiques it.
- It is enforced by no check this repository runs today; a reviewer asks of each name, "is this a file in disguise?".
