/* For license and copyright information please see the LEGAL file in the code repository */

package qmcp

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID    //
	Min() uint64                    //
	Max() uint64                    //
	SaveTime() protocol.Time        // Save time
	RequestID() urp.UserRequestUUID //
}
