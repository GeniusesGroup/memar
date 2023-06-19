/* For license and copyright information please see the LEGAL file in the code repository */

package qadp

import (
	"libgo/protocol"

	qap "org/modules/question_answer/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AnswerID() qap.AnswerUUID       //
	Answer() string                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

// QuestionAnswerDescriptive_Type_Anonymous
