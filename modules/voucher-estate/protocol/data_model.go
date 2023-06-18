/* For license and copyright information please see the LEGAL file in the code repository */

package vep

import (
	"libgo/protocol"

	eblp "org/modules/estate-building-location/protocol"
	ebp "org/modules/estate-building/protocol"
	ep "org/modules/estate/protocol"
	urp "org/modules/user-request/protocol"
	vp "org/modules/voucher/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel is proper or appropriate location indicate specific area not specific location
// It's rule depend on products in invoices e.g. source or destination of taxi as a service(product).
type DataModel interface {
	VoucherID() vp.VoucherUUID                     //
	EstateID() ep.EstateUUID                       //
	BuildingID() ebp.BuildingUUID                  //
	BuildingLocationID() eblp.BuildingLocationUUID //
	SaveTime() protocol.Time                       //
	RequestID() urp.UserRequestUUID                //
}
