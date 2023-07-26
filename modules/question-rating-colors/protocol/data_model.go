/* For license and copyright information please see the LEGAL file in the code repository */

package qrcp

import (
	"memar/protocol"

	qp "org/modules/question/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID
	Colors() []protocol.RGB

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
