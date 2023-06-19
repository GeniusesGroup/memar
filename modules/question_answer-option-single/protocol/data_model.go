/* For license and copyright information please see the LEGAL file in the code repository */

package qapsp

import (
	"libgo/protocol"

	qap "org/modules/question_answer/protocol"
	qop "org/modules/question_option/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AnswerID() qap.AnswerUUID       //
	Answer() qop.QuestionOptionUUID //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
