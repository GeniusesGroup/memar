/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type QuestionUUID protocol.UUID

// Question indicate the domain record data fields.
type Question interface {
	QuestionID() QuestionUUID       //
	Type() Question_Type            //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID // user-request domain
}

type Question_Type uint16

const (
	Question_Type_Unset      Question_Type = 0
	Question_Type_StandAlone Question_Type = (1 << iota) // not part of a questionnaire
	Question_Type_Quiz
	Question_Type_Anonymous
	Question_Type_Duration
	Question_Type_ForceToAnswer
	Question_Type_AllowToEdit

	// Multiple below flags can be turned on.
	Question_Type_YesNo // True/False
	Question_Type_SingleChoice
	Question_Type_MultipleChoice
	Question_Type_FillInTheBlank
	Question_Type_Descriptive
	Question_Type_Rating
)
