/* For license and copyright information please see the LEGAL file in the code repository */

package qrtp

import (
	"memar/protocol"

	qp "org/modules/questionnaire/protocol"
	tp "org/modules/task/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireID() qp.QuestionnaireUUID
	TaskID() tp.TaskUUID
	Type() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// LIST_QuestionnaireIDs_By_TaskID_AND_Type(taskID tp.TaskUUID, t Type, offset, limit uint64) (questionnaireIDs []qp.QuestionnaireUUID, nv protocol.NumberOfVersion, err protocol.Error)
