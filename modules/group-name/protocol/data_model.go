/* For license and copyright information please see the LEGAL file in the code repository */

// It is not the group title as display name, It is the unique group name.
package gnp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	gp "org/modules/group/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	GroupID() gp.GroupUUID
	Name() Name
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
