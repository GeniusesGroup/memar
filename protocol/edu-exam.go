/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type EducationExamUUID = protocol.UUID

// EducationExam indicate the domain record data fields.
type EducationExam interface {
	ExamID() EducationExamUUID                   //
	UserID() UserUUID                            //
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	Time() protocol.Time                         // save time
	RequestID() urp.UserRequestUUID              //
}
