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
	RequestID() urp.UserRequestUUID // user-request domain
}

// QuestionAnswerDescriptive_Type_Anonymous

type  QuestionAnswerDescriptive_StorageServices interface {
	Save(f QuestionAnswerDescriptive) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(answerID AnswerUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(answerID AnswerUUID, vo protocol.VersionOffset) (f QuestionAnswerDescriptive, nv protocol.NumberOfVersion, err protocol.Error)

}
