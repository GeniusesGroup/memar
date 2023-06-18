/* For license and copyright information please see the LEGAL file in the code repository */

package qrtp

import (
	"libgo/protocol"

	qp "org/modules/questionnaire/protocol"
	tp "org/modules/task/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireID() qp.QuestionnaireUUID //
	TaskID() tp.TaskUUID                   //
	Type() Type                            //
	SaveTime() protocol.Time               //
	RequestID() urp.UserRequestUUID        //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_Creator
	Type_Pending
)

// LIST_QuestionnaireIDs_By_TaskID_AND_Type(taskID tp.TaskUUID, t Type, offset, limit uint64) (questionnaireIDs []qp.QuestionnaireUUID, nv protocol.NumberOfVersion, err protocol.Error)
