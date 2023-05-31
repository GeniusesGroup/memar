/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionAnswerMatching indicate the domain record data fields.
type QuestionAnswerMatching interface {
	QuestionID() QuestionUUID       //
	Matches() []QuestionOptionUUID  //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type QuestionAnswerMatching_StorageServices interface {
	Save(f QuestionAnswerMatching) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (f QuestionAnswerMatching, nv protocol.NumberOfVersion, err protocol.Error)
}
