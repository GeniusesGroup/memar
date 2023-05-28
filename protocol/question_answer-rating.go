/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionAnswerRating indicate the domain record data fields.
type QuestionAnswerRating interface {
	AnswerID() AnswerUUID           //
	Answer() uint8                  //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type QuestionAnswerRating_StorageServices interface {
	Save(f QuestionAnswerRating) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(answerID AnswerUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(answerID AnswerUUID, vo protocol.VersionOffset) (f QuestionAnswerRating, nv protocol.NumberOfVersion, err protocol.Error)
}
