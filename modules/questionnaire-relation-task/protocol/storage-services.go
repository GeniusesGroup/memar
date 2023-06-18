/* For license and copyright information please see the LEGAL file in the code repository */

package qrtp

import (
	"libgo/protocol"

	qp "org/modules/questionnaire/protocol"
	tp "org/modules/task/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionnaireID qp.QuestionnaireUUID, taskID tp.TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionnaireID qp.QuestionnaireUUID, taskID tp.TaskUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_QuestionnaireIDs_By_TaskID(taskID tp.TaskUUID, offset, limit uint64) (questionnaireIDs []qp.QuestionnaireUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_TaskIDs_BY_QuestionnaireID(questionnaireID qp.QuestionnaireUUID, offset, limit uint64) (taskIDs []tp.TaskUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
