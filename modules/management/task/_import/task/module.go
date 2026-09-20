/* For license and copyright information please see the LEGAL file in the code repository */

package domain

import (
	"libgo/module"
	"libgo/protocol"
)

var ModuleName = moduleName{
	Name: "",
}

type moduleName struct {
	module.Module
}

func init() {
	protocol.App.RegisterModule(&ModuleName)
}
