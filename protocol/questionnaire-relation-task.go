/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionnaireTaskRelation indicate the domain record data fields.
type QuestionnaireTaskRelation interface {
	QuestionnaireID() QuestionnaireUUID   //
	TaskID() TaskUUID                     //
	Type() QuestionnaireTaskRelation_Type //
	Time() protocol.Time                  // save time
	RequestID() urp.UserRequestUUID       //
}

type QuestionnaireTaskRelation_StorageServices interface {
	Save(dm QuestionnaireTaskRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionnaireID QuestionnaireUUID, taskID TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionnaireID QuestionnaireUUID, taskID TaskUUID, vo protocol.VersionOffset) (dm QuestionnaireTaskRelation, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_QuestionnaireIDs_By_TaskID(taskID TaskUUID, offset, limit uint64) (questionnaireIDs []QuestionnaireUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_TaskIDs_BY_QuestionnaireID(questionnaireID QuestionnaireUUID, offset, limit uint64) (taskIDs []TaskUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type QuestionnaireTaskRelation_Type uint8

const (
	QuestionnaireTaskRelation_Type_Unset QuestionnaireTaskRelation_Type = iota
	QuestionnaireTaskRelation_Type_Creator
	QuestionnaireTaskRelation_Type_Pending
)

// LIST_QuestionnaireIDs_By_TaskID_AND_Type(taskID TaskUUID, t QuestionnaireTaskRelation_Type, offset, limit uint64) (questionnaireIDs []QuestionnaireUUID, nv protocol.NumberOfVersion, err protocol.Error)
