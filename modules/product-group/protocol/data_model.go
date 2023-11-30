/* For license and copyright information please see the LEGAL file in the code repository */

package pgp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	gp "org/modules/group/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID
	GroupID() gp.GroupUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
