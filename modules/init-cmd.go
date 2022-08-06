/* For license and copyright information please see LEGAL file in ChaparKhane repository */

package modules

import (
	"github.com/GeniusesGroup/libgo/cli"
)

var RootCommand rootCommand

type rootCommand struct {
	cli.Command
}

// Init use to initialize all services and register them in the RootCommand.
func (rc *rootCommand) Init() {
	rc.Command.Init("org", "org <command> [arguments]", nil, false)

	// project.Command.Init(rc)

	// rc.Command.SetSubCommands()
}
