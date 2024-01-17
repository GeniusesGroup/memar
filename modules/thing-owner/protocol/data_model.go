/* For license and copyright information please see the LEGAL file in the code repository */

package top

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	tp "org/modules/thing/protocol"
	up "org/modules/user/protocol"
)

// ThingOwner
// e.g. Vehicle is a conveyance that transports people or objects
type ThingOwner interface {
	ThingID() tp.ThingUUID
	OwnerID() up.UserUUID

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
