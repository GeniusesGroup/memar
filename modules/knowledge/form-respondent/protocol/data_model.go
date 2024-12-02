/* For license and copyright information please see the LEGAL file in the code repository */

package qrp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	qop "org/modules/questionnaire-order/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireRespondentID() QuestionnaireRespondentUUID
	QuestionnaireOrderID() qop.QuestionnaireOrderUUID
	AnswerBy() up.UserUUID
	FillBy() up.UserUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
