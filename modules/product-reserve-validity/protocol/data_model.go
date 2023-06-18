/* For license and copyright information please see the LEGAL file in the code repository */

package prvp

import (
	"libgo/protocol"

	pp "org/modules/product/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID      //
	Duration() protocol.Duration    // from add to invoice time
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
