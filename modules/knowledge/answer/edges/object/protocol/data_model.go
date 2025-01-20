/* For license and copyright information please see the LEGAL file in the code repository */

package qaop

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	op "org/modules/object/protocol"
	qap "org/modules/question_answer/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AnswerID() qap.AnswerUUID
	AnswerObject() op.ObjectUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
