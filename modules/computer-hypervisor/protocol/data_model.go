/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"memar/protocol"

	cp "org/modules/computer/protocol"
)

type DataModel interface {
	ComputerID() cp.UUID
	Hypervisor() string // TODO::: name, version, ...

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
