/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionAnswerDescriptive indicate the domain record data fields.
type QuestionAnswerDescriptive interface {
	AnswerID() AnswerUUID           //
	Answer() string                 //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

// QuestionAnswerDescriptive_Type_Anonymous

type QuestionAnswerDescriptive_StorageServices interface {
	Save(dm QuestionAnswerDescriptive) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(answerID AnswerUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(answerID AnswerUUID, vo protocol.VersionOffset) (dm QuestionAnswerDescriptive, nv protocol.NumberOfVersion, err protocol.Error)
}
