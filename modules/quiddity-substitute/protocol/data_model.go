/* For license and copyright information please see the LEGAL file in the code repository */

package qsp

import (
	"libgo/protocol"

	qp "org/modules/quiddity/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// or similar product
type DataModel interface {
	QuiddityID() qp.QuiddityUUID    //
	Priority() uint64               // Substitute priority
	SubstituteID() qp.QuiddityUUID  //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
