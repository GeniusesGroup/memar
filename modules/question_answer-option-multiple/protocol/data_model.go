/* For license and copyright information please see the LEGAL file in the code repository */

package qaomp

import (
	"libgo/protocol"

	qap "org/modules/question_answer/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AnswerID() qap.AnswerUUID         //
	Answer() []qop.QuestionOptionUUID //
	SaveTime() protocol.Time          // Save time
	RequestID() urp.UserRequestUUID   //
}

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(answerID qap.AnswerUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(answerID qap.AnswerUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
