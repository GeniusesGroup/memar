#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

# For license and copyright information please see the LEGAL file in the code repository

"""mcp/ is a regular package, unlike the other folders of the scripts, and only for its name.

The MCP SDK installs a package named `mcp` too. A folder with no `__init__.py` is a namespace
package, which Python takes only when no regular package of that name is found anywhere on the
search path, so on a machine with the SDK `mcp.mcp` would be looked for inside the SDK and not
found. As a regular package this folder is found first, because the router puts this shelf at the
front of the search path.
"""
