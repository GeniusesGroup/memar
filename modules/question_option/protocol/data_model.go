/* For license and copyright information please see the LEGAL file in the code repository */

package qop

import (
	"memar/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionOptionID() QuestionOptionUUID
	Type() Type
	Significance_Positive() uint64
	Significance_Negative() uint64

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
