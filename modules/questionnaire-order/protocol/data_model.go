/* For license and copyright information please see the LEGAL file in the code repository */

package qop

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	qp "org/modules/question/protocol"
	qrp "org/modules/questionnaire/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireOrderID() QuestionnaireOrderUUID
	QuestionnaireID() qrp.QuestionnaireUUID
	Questions() []qp.QuestionUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
