/* For license and copyright information please see the LEGAL file in the code repository */

package exqdp

import (
	"libgo/protocol"

	eeqp "org/modules/edu-exam-question/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() eeqp.EducationQuestionUUID //
	Language() protocol.Language            //
	Question() string                       // Content+Presentation(HTML, CSS)
	CorrectAnswer() string                  // A||B, A&B
	SaveTime() protocol.Time                //
	RequestID() urp.UserRequestUUID         //
}
