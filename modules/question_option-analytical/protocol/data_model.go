/* For license and copyright information please see the LEGAL file in the code repository */

package qoap

import (
	"memar/math/per"
	"memar/protocol"

	qop "org/modules/question_option/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionOptionID() qop.QuestionOptionUUID
	Progress() per.Myriad // =~ AmountOfProgress,  EarnGoal
	TimeFrame() protocol.Duration

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
