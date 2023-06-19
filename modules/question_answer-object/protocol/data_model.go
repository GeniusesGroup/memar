/* For license and copyright information please see the LEGAL file in the code repository */

package qaop

import (
	"libgo/protocol"

	op "org/modules/object/protocol"
	qap "org/modules/question_answer/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AnswerID() qap.AnswerUUID       //
	AnswerObject() op.ObjectUUID    //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
