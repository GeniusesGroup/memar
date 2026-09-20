/* For license and copyright information please see the LEGAL file in the code repository */

package pnp

import (
	decimal_p "memar/math/decimal/protocol"
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	product_p "org/modules/economics/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	product_p.Field_ProductID
	Minimum() decimal_p.Quantity             // Minimum number of sale to serve the service e.g. cinema wouldn't play movie, ...
	Maximum() decimal_p.Quantity             // Maximum number can be served to buyers e.g. cinema tickets, panic-room game, ...
	MaximumInvoiceByBuy() decimal_p.Quantity // Maximum buy e.g. hotel room, panic-room game, ... that must limit by buyer.

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
