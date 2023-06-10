/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// EducationQuestionDescription indicate the domain record data fields.
type EducationQuestionDescription interface {
	QuestionID() EducationQuestionUUID //
	Language() protocol.Language       //
	Question() string                  // Content+Presentation(HTML, CSS)
	CorrectAnswer() string             // A||B, A&B
	Time() protocol.Time               // save time
	RequestID() urp.UserRequestUUID    //
}
