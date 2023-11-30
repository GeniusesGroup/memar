/* For license and copyright information please see the LEGAL file in the code repository */

package qrlp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	qp "org/modules/question/protocol"
	qdp "org/modules/quiddity/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID
	Labels() []qdp.QuiddityUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
