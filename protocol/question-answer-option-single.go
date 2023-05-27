/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionAnswerOptionSingle indicate the domain record data fields.
type QuestionAnswerOptionSingle interface {
	AnswerID() AnswerUUID           //
	Answer() QuestionOptionUUID     //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID // user-request domain
}


type  QuestionAnswerOptionSingle_StorageServices interface {
	Save(f QuestionAnswerOptionSingle) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(answerID AnswerUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(answerID AnswerUUID, vo protocol.VersionOffset) (f QuestionAnswerOptionSingle, nv protocol.NumberOfVersion, err protocol.Error)

}
