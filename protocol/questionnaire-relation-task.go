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
	Save(pc QuestionnaireTaskRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(taskID TaskUUID, questionnaireID QuestionnaireUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(taskID TaskUUID, questionnaireID QuestionnaireUUID, vo protocol.VersionOffset) (pc QuestionnaireTaskRelation, nv protocol.NumberOfVersion, err protocol.Error)
}

type QuestionnaireTaskRelation_Type uint8

const (
	QuestionnaireTaskRelation_Type_Unset QuestionnaireTaskRelation_Type = iota
	QuestionnaireTaskRelation_Type_Creator
	QuestionnaireTaskRelation_Type_Pending
)
