/* For license and copyright information please see the LEGAL file in the code repository */

package pap

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ep "org/modules/estate/protocol"
	prp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel is proper or appropriate location indicate specific area not specific location e.g. Taxi, ...
type DataModel interface {
	ProductID() prp.ProductUUID
	EstateID() ep.EstateUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
