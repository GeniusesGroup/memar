#

## Model

### Graph vertex
Base on [DDD] We MUST choose some limited thing to be top level modules labels.

### Graph Edges
Graph Edges use as labels to relate two vertices or as a graph loop.

### Graph loop
In graph theory, a [loop](https://en.wikipedia.org/wiki/Loop_(graph_theory)) (also called a self-loop or a buckle) is an edge that connects a vertex to itself. A simple graph contains no loops.

#### Examples
- `Commodity` is an edge for any `product` vertex but not link the `product` to any other `thing` in the system.

### Pitfalls
- Labels for bad relation. 
  - `user1` is `creator` of `comment1` with `email` label and `user2` is `creator` of `comment2` with `email` label that `comment2` is `reply` for `comment1` so we can use `REPLIED_TO` label as `user2` `REPLIED_TO` `comment1`, But it is better to use as `comment2` `REPLY_TO` `comment1`

### Fields
- Some edges CAN carry some data such as `time` or `status` or ...
- They will be introduces in each package or in `memar`

## Top or thing Levels labels

Just some limited labels can be top or quiddity Levels labels. We MUST think very deeply to add any label here e.g. `project` is just a label for `task` and MUST NOT add as thing level label.

`TODO:::` Each UUID can use in more than one vertex category.
e.g. `product` UUID is as `text` UUID for a product.
e.g. `product` UUID use as `group` for a product as default chat timeline (comments)
If above is true, we can assume that default text as `loop edge` is title for each vertex.

## Idea backlog

Nothing below is ratified.

### Module manifest
- **Idea**: a published module carries a manifest: name, description, documentation URL, git repository, files to include and exclude, compilers (name and version), install and uninstall scripts, and requirements split into direct, indirect, and test-only.
- **Review questions**: is that manifest a document of this repository's module layout, or a package format of its own? The sketch nested a full module descriptor inside each direct requirement. Does a requirement name an existing module, or copy that module's manifest?
