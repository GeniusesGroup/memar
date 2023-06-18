/* For license and copyright information please see the LEGAL file in the code repository */

package pgp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	pp "org/modules/product/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID //
	GroupID() gp.GroupUUID     //
	Status() Status
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status
