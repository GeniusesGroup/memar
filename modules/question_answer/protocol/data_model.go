/* For license and copyright information please see the LEGAL file in the code repository */

package qap

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AnswerID() AnswerUUID           //
	QuestionID() qp.QuestionUUID    //
	AnswerBy() up.UserUUID          //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
