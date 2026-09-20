// go:build gui

/* For license and copyright information please see the LEGAL file in the code repository */

package domain

import (
	"libgo/protocol"
)

func RegisterPages() {
	protocol.App.RegisterPage()
}

func RegisterWidgets() {
	protocol.App.RegisterPage()
}
