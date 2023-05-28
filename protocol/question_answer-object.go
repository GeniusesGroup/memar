/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionAnswerObject indicate the domain record data fields.
type QuestionAnswerObject interface {
	AnswerID() AnswerUUID           //
	AnswerObject() ObjectUUID       //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type QuestionAnswerObject_StorageServices interface {
	Save(f QuestionAnswerObject) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(answerID AnswerUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(answerID AnswerUUID, vo protocol.VersionOffset) (f QuestionAnswerObject, nv protocol.NumberOfVersion, err protocol.Error)
}
