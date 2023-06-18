/* For license and copyright information please see the LEGAL file in the code repository */

package qoop

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
	qop "org/modules/question_option/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID            //
	CorrectOrder() []qop.QuestionOptionUUID //
	SaveTime() protocol.Time                // Save time
	RequestID() urp.UserRequestUUID         //
}
