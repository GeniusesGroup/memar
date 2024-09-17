/* For license and copyright information please see the LEGAL file in the code repository */

package qap

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	qp "org/modules/question/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AnswerID() AnswerUUID
	QuestionID() qp.QuestionUUID
	AnswerBy() up.UserUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
