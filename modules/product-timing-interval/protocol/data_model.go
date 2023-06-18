/* For license and copyright information please see the LEGAL file in the code repository */

package ptip

import (
	"libgo/protocol"

	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// e.g. flight duration, doctor visit, carwash, ...
type DataModel interface {
	ProductID() pp.ProductUUID      //
	Minimum() protocol.Duration     // Minimum time duration for this service
	Expected() protocol.Duration    // Expected time duration for this service
	Maximum() protocol.Duration     // Maximum time duration for this service
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
