/* For license and copyright information please see the LEGAL file in the code repository */

package iip

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ip "org/modules/invoice/protocol"
	pp "org/modules/product/protocol"
	qrtp "org/modules/quiddity-relation-type/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID
	ProductID() pp.ProductUUID
	IngredientID() pp.ProductUUID
	IngredientUnit() qrtp.QuiddityRelationTypeUUID
	Quantity() uint64 // decimal >> 1.5 >> 1.2 >> 10 >> 0
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
