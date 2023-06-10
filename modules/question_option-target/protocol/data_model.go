/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionOptionGoal indicate the domain record data fields.
type QuestionOptionTarget interface {
	QuestionOptionID() QuestionOptionUUID //
	Target() protocol.PerMyriad           // =~ Goal
	TimeFrame() protocol.Duration         // =~ Interval, TimeSpan, TimeFrame, TimePeriod,
	Time() protocol.Time                  // Save time
	RequestID() urp.UserRequestUUID       //
}

type QuestionOptionGoal_StorageServices interface {
	Save(dm QuestionOptionTarget) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionOptionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionOptionID QuestionUUID, vo protocol.VersionOffset) (dm QuestionOptionTarget, nv protocol.NumberOfVersion, err protocol.Error)
}
