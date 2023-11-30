/* For license and copyright information please see the LEGAL file in the code repository */

package qamp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	qp "org/modules/question/protocol"
	qop "org/modules/question_option/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID
	Matches() []qop.QuestionOptionUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
