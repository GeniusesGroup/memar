/* For license and copyright information please see the LEGAL file in the code repository */

package plp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	org "org/modules/org/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID
	OrgID() org.OrgUUID
	Type() Type

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
