/* For license and copyright information please see the LEGAL file in the code repository */

package ptvp

import (
	"libgo/protocol"

	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// flight departure and arrival time, concert start and end time, ...
type DataModel interface {
	ProductID() pp.ProductUUID      //
	Start() protocol.Time           //
	End() protocol.Time             //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
