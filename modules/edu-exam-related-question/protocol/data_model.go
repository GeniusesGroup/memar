/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	eeqp "org/modules/edu-exam-question/protocol"
	exp "org/modules/edu-exam/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	SuggesterID() up.UserUUID               //
	ExamID() exp.EducationExamUUID          //
	Priority() uint64                       //
	QuestionID() eeqp.EducationQuestionUUID //
	SaveTime() protocol.Time                //
	RequestID() urp.UserRequestUUID         //
}
