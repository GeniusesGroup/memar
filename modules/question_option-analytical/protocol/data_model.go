/* For license and copyright information please see the LEGAL file in the code repository */

package qoap

import (
	"libgo/protocol"

	qop "org/modules/question_option/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionOptionID() qop.QuestionOptionUUID //
	Progress() protocol.PerMyriad             // =~ AmountOfProgress,  EarnGoal
	TimeFrame() protocol.Duration             //
	SaveTime() protocol.Time                  //
	RequestID() urp.UserRequestUUID           //
}
