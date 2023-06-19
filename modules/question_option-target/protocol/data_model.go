/* For license and copyright information please see the LEGAL file in the code repository */

package qotp

import (
	"libgo/protocol"

	qop "org/modules/question_option/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionOptionID() qop.QuestionOptionUUID //
	Target() protocol.PerMyriad               // =~ Goal
	TimeFrame() protocol.Duration             // =~ Interval, TimeSpan, TimeFrame, TimePeriod,
	SaveTime() protocol.Time                  //
	RequestID() urp.UserRequestUUID           //
}
