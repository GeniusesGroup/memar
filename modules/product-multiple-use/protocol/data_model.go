/* For license and copyright information please see the LEGAL file in the code repository */

package pmup

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID      //
	Maximum() uint64                // Maximum time this service can be served to buyer
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

