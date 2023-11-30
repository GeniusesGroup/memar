/* For license and copyright information please see the LEGAL file in the code repository */

package qspp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	qp "org/modules/questionnaire/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireID() qp.QuestionnaireUUID
	// TODO::: embed or copy??
	protocol.Time

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
