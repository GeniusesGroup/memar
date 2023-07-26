/* For license and copyright information please see the LEGAL file in the code repository */

package qspp

import (
	"memar/protocol"

	qp "org/modules/questionnaire/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireID() qp.QuestionnaireUUID
	// TODO::: embed or copy??
	protocol.Time

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
