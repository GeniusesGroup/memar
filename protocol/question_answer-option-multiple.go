/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionAnswerOptionMultiple indicate the domain record data fields.
type QuestionAnswerOptionMultiple interface {
	AnswerID() AnswerUUID           //
	Answer() []QuestionOptionUUID   //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type QuestionAnswerOptionMultiple_StorageServices interface {
	Save(f QuestionAnswerOptionMultiple) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(answerID AnswerUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(answerID AnswerUUID, vo protocol.VersionOffset) (f QuestionAnswerOptionMultiple, nv protocol.NumberOfVersion, err protocol.Error)
}
