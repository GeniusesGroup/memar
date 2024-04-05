/* For license and copyright information please see the LEGAL file in the code repository */

// Voucher estate is proper or appropriate location indicate specific area not specific location
// It's rule depend on products in invoices e.g. source or destination of taxi as a service(product).
package vep

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	eblp "org/modules/estate-building-location/protocol"
	ebp "org/modules/estate-building/protocol"
	ep "org/modules/estate/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	VoucherID() vp.VoucherUUID
	EstateID() ep.EstateUUID
	BuildingID() ebp.BuildingUUID
	BuildingLocationID() eblp.BuildingLocationUUID

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
