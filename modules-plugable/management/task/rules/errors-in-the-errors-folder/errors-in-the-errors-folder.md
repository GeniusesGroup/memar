# Task Rule — The errors of a module are declared in its errors folder
Status: Draft

## The rule
The errors of a module are declared in the module's `errors` folder, as Khayyam, and nowhere else: not in `protocol`, not in a service's file, not in the realization. A realization raises, returns or matches an error only by the declaration that folder holds and makes no error type of its own. Each error is a type with the [`detail.kh`](../../../../../modules/computer/type/protocol/detail.kh) methods. An error the realization needs and the folder lacks is declared there first, as [abstraction first](../abstraction-first-in-khayyam/abstraction-first-in-khayyam.md) says. A module with no errors has no `errors` folder. The shape follows the modules that already declare theirs, for example [`errors.kh` of `index`](../../../../computer/memory/store/index/errors/errors.kh).

## Why it exists
An error is part of what a module says of itself; one placed in `protocol` or in a Python file cannot be found where a reader and a tool look for it, and its `detail.kh` methods are not written. The memory-layer task put `Unavailability` in `protocol/store.py`.

## How a check would run
Search a module for the declaration of an error type or an error value outside its `errors` folder, and for a module whose realization raises an error that has no `errors` folder. This repository runs no automatic check of it today.
