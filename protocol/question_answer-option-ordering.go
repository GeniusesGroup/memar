/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionAnswerOptionsOrdering indicate the domain record data fields.
type QuestionAnswerOptionsOrdering interface {
	QuestionID() QuestionUUID           //
	OptionsOrder() []QuestionOptionUUID //
	Time() protocol.Time                // Save time
	RequestID() urp.UserRequestUUID     //
}

type QuestionAnswerOptionsOrdering_StorageServices interface {
	Save(f QuestionAnswerOptionsOrdering) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (f QuestionAnswerOptionsOrdering, nv protocol.NumberOfVersion, err protocol.Error)
}
