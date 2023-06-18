/* For license and copyright information please see the LEGAL file in the code repository */

package qip

import (
	"libgo/protocol"

	qp "org/modules/quiddity/protocol"
	op "org/modules/object/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// Icon or emoji use in many domains e.g. category, departments, ...
type DataModel interface {
	QuiddityID() qp.QuiddityUUID    //
	Icon() op.ObjectUUID            //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
