/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionOptionAnalytical indicate the domain record data fields.
type QuestionOptionAnalytical interface {
	QuestionOptionID() QuestionOptionUUID //
	Progress() protocol.PerMyriad         // =~ AmountOfProgress,  EarnGoal
	TimeFrame() protocol.Duration         //
	Time() protocol.Time                  // Save time
	RequestID() urp.UserRequestUUID       //
}

type QuestionOptionAnalytical_StorageServices interface {
	Save(f QuestionOptionAnalytical) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (f QuestionOptionAnalytical, nv protocol.NumberOfVersion, err protocol.Error)
}
