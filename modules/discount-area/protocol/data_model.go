/* For license and copyright information please see the LEGAL file in the code repository */

package dap

import (
	"libgo/protocol"

	dp "org/modules/discount/protocol"
	ep "org/modules/estate/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel is proper or appropriate location indicate specific area not specific location
// It's rule depend on products in invoices e.g. source or destination of taxi as a service(product).
type DataModel interface {
	DiscountID() dp.DiscountUUID //
	EstateID() ep.EstateUUID
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
