/* For license and copyright information please see the LEGAL file in the code repository */

package qrlp

import (
	"memar/protocol"

	lp "org/modules/label/protocol"
	qp "org/modules/question/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID
	Label() lp.LabelUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
