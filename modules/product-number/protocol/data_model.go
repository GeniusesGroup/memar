/* For license and copyright information please see the LEGAL file in the code repository */

package pnp

import (
	"libgo/protocol"

	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID      //
	Minimum() uint64                // Minimum number of sale to serve the service e.g. cinema wouldn't play movie, ...
	Maximum() uint64                // Maximum number can be served to buyers e.g. cinema tickets, panic-room game, ...
	MaximumInvoiceByBuy() uint64    // Maximum buy e.g. hotel room, panic-room game, ... that must limit by buyer.
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
