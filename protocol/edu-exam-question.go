/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type EducationQuestionUUID = protocol.UUID

// EducationKnowledgeUnitQuestion indicate the domain record data fields.
type EducationKnowledgeUnitQuestion interface {
	QuestionID() EducationQuestionUUID           // don't point to quiddity title na don't set title
	UserID() UserUUID                            //
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	Type() EducationKnowledgeUnitQuestion_Type   //
	Time() protocol.Time                         // save time
	RequestID() urp.UserRequestUUID              //
}

type EducationKnowledgeUnitQuestion_Type uint8

const (
	EducationKnowledgeUnitQuestion_Type_Unset EducationKnowledgeUnitQuestion_Type = iota
	EducationKnowledgeUnitQuestion_Type_SingleChoice
	EducationKnowledgeUnitQuestion_Type_MultipleChoice
	EducationKnowledgeUnitQuestion_Type_Descriptive
)
