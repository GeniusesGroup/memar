/* For license and copyright information please see the LEGAL file in the code repository */

package pcp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	cp "org/modules/content/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID
	ContentID() cp.ContentUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
