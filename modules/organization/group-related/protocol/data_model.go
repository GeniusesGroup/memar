/* For license and copyright information please see the LEGAL file in the code repository */

package grp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	gp "org/modules/group/protocol"
)

// GroupRelated indicate the domain record data fields.
type GroupRelated interface {
	GroupID() gp.GroupUUID
	RelatedGroupID() gp.GroupUUID // Use to categorize and graph groups
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
