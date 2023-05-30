/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type AnswerUUID protocol.UUID

// QuestionAnswer indicate the domain record data fields.
type QuestionAnswer interface {
	AnswerID() AnswerUUID           //
	QuestionID() QuestionUUID       //
	AnswerBy() up.UserUUID          //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type QuestionAnswer_StorageServices interface {
	Save(f QuestionAnswer) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(answerID AnswerUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(answerID AnswerUUID, vo protocol.VersionOffset) (f QuestionAnswer, nv protocol.NumberOfVersion, err protocol.Error)
}
