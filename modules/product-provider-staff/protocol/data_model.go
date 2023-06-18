/* For license and copyright information please see the LEGAL file in the code repository */

package ppsp

import (
	"libgo/protocol"

	pp "org/modules/product/protocol"
	qsp "org/modules/quiddity-status/protocol"
	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID //
	StaffID() sp.StaffUUID     //
	Status() Status
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

// related UserIDs by StaffID use to get Coordinate(domain)
