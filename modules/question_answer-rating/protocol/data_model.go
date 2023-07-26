/* For license and copyright information please see the LEGAL file in the code repository */

package qarp

import (
	"memar/protocol"

	qap "org/modules/question_answer/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AnswerID() qap.AnswerUUID
	Answer() Answer

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
