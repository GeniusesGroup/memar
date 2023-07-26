/* For license and copyright information please see the LEGAL file in the code repository */

package qrrtp

import (
	"memar/protocol"

	qrp "org/modules/questionnaire-respondent/protocol"
	tp "org/modules/task/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionnaireRespondentID qrp.QuestionnaireRespondentUUID, taskID tp.TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionnaireRespondentID qrp.QuestionnaireRespondentUUID, taskID tp.TaskUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_QuestionnaireRespondentIDs_BY_TaskID(taskID tp.TaskUUID, offset, limit uint64) (DataModel []qrp.QuestionnaireRespondentUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_TaskIDs_BY_QuestionnaireRespondentID(QuestionnaireRespondentID qrp.QuestionnaireRespondentUUID, offset, limit uint64) (taskIDs []tp.TaskUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
