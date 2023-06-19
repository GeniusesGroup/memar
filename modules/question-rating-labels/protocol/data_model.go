/* For license and copyright information please see the LEGAL file in the code repository */

package qrlp

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
	qdp "org/modules/quiddity/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID    //
	Labels() []qdp.QuiddityUUID     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
