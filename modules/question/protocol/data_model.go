/* For license and copyright information please see the LEGAL file in the code repository */

package qp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TODO::: dynamic data in question?? text substitution, text piping

// DataModel indicate the domain record data fields.
// DataModel text, videos, images, ... save in Comment domains.
type DataModel interface {
	QuestionID() QuestionUUID       //
	Type() Type                     //
	SaveTime() protocol.Time        // Save time
	RequestID() urp.UserRequestUUID //
}

type Type uint32

const (
	Type_Unset      Type = 0
	Type_StandAlone Type = (1 << iota) // not part of a questionnaire
	Type_Quiz
	Type_Anonymous
	Type_Duration
	Type_ForceToAnswer
	Type_AllowToEdit
	Type_MaxAttempt
	Type_Analytical

	// Multiple below flags can be turned on.
	Type_YesNo // True/False
	Type_SingleChoice
	Type_MultipleChoice
	Type_Ordering // options, options-ordering
	// Matching items require students to match a series of stems or premises to a response or principle.
	// They consist of a set of directions, a column of statements and a column of responses.
	// Matching questions are really a variation of the multiple choice format.
	Type_Matching
	Type_FillInTheBlank
	Type_Descriptive
	Type_Rating
	Type_Object
)

type Question_GUI_Widget interface {
}
