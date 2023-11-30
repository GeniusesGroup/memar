/* For license and copyright information please see the LEGAL file in the code repository */

package qrp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	qp "org/modules/question/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID
	Type() Type
	Max() uint8

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
