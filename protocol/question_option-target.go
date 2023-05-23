/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionOptionGoal indicate the domain record data fields.
type QuestionOptionGoal interface {
	QuestionOptionID() QuestionOptionUUID //
	Target() protocol.PerMyriad           // =~ Goal
	TimeFrame() protocol.Duration         // =~ Interval, TimeSpan, TimeFrame, TimePeriod,
	Time() protocol.Time                  // Save time
	RequestID() urp.UserRequestUUID       // user-request domain
}
