/* For license and copyright information please see the LEGAL file in the code repository */

package itp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ip "org/modules/invite/protocol"
	tp "org/modules/task/protocol"
)

// TODO::: Optional module

// DataModel indicate the domain record data fields.
type DataModel interface {
	InviteID() ip.InviteUUID
	TaskID() tp.TaskUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
