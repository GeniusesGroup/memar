/* For license and copyright information please see the LEGAL file in the code repository */

package qsp

import (
	"memar/protocol"

	qp "org/modules/questionnaire/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireID() qp.QuestionnaireUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
