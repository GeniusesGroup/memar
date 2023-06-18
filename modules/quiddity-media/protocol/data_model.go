/* For license and copyright information please see the LEGAL file in the code repository */

package qmp

import (
	"libgo/protocol"

	op "org/modules/object/protocol"
	qp "org/modules/quiddity/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	QuiddityID() qp.QuiddityUUID    //
	Priority() uint64               // Media priority
	ObjectID() op.ObjectUUID        //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
