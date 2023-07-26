/* For license and copyright information please see the LEGAL file in the code repository */

package qotp

import (
	"memar/math/per"
	"memar/protocol"

	qop "org/modules/question_option/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionOptionID() qop.QuestionOptionUUID
	Target() per.Myriad           // =~ Goal
	TimeFrame() protocol.Duration // =~ Interval, TimeSpan, TimeFrame, TimePeriod,

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
