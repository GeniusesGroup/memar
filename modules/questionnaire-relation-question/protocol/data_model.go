/* For license and copyright information please see the LEGAL file in the code repository */

package qrqp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	qp "org/modules/question/protocol"
	qrp "org/modules/questionnaire/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireID() qrp.QuestionnaireUUID
	QuestionID() qp.QuestionUUID
	Significance_Positive() uint64
	Significance_Negative() uint64
	Type() Type

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// LIST_QuestionIDs_BY_QuestionnaireID(questionnaireID qp.QuestionnaireUUID, offset, limit uint64) (questionIDs []qp.QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)
