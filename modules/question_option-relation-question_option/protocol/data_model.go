/* For license and copyright information please see the LEGAL file in the code repository */

package qorqop

import (
	"memar/protocol"

	qop "org/modules/question_option/protocol"
)

// In most cases just when Type_Criterion flag is on.

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionOptionID() qop.QuestionOptionUUID
	RelationID() qop.QuestionOptionUUID
	// Type()

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
