/* For license and copyright information please see the LEGAL file in the code repository */

package eeqp

import (
	"libgo/protocol"

	ekup "org/modules/edu-knowledge_unit/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() EducationQuestionUUID                // don't point to quiddity title na don't set title
	UserID() up.UserUUID                              //
	KnowledgeUnitID() ekup.EducationKnowledgeUnitUUID //
	Type() Type                                       //
	SaveTime() protocol.Time                          //
	RequestID() urp.UserRequestUUID                   //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_SingleChoice
	Type_MultipleChoice
	Type_Descriptive
)
