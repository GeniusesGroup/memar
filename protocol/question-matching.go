/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionMatching indicate the domain record data fields.
type QuestionMatching interface {
	QuestionID() QuestionUUID       //
	Matches() []QuestionOptionUUID  //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type QuestionMatching_StorageServices interface {
	Save(dm QuestionMatching) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (dm QuestionMatching, nv protocol.NumberOfVersion, err protocol.Error)
}

