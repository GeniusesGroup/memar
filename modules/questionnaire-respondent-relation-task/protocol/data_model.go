/* For license and copyright information please see the LEGAL file in the code repository */

package qrrtp

import (
	"memar/protocol"

	qrp "org/modules/questionnaire-respondent/protocol"
	tp "org/modules/task/protocol"
)

// It is announcement that user tell the system to start answer to questions.

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireRespondentID() qrp.QuestionnaireRespondentUUID
	TaskID() tp.TaskUUID
	Type() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// FindByTaskIDAndType(taskID tp.TaskUUID, t Type, offset, limit uint64) (QuestionnaireRespondentIDs []qrp.QuestionnaireRespondentUUID, nv protocol.NumberOfVersion, err protocol.Error)
