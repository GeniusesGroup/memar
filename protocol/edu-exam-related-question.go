/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// EducationExamRelatedQuestion indicate the domain record data fields.
type EducationExamRelatedQuestion interface {
	SuggesterID() protocol.UserID      //
	ExamID() EducationExamUUID         //
	Priority() uint64                  //
	QuestionID() EducationQuestionUUID //
	Time() protocol.Time               // save time
	RequestID() UserRequestUUID        // user-request domain
}
