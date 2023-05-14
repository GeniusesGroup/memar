/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type QuestionOptionUUID protocol.UUID

// QuestionOption indicate the domain record data fields.
type QuestionOption interface {
	QuestionOptionID() QuestionOptionUUID //
	Type() QuestionOption_Type            //
	Significance_Positive() uint64        //
	Significance_Negative() uint64        //
	Time() protocol.Time                  // Save time
	RequestID() urp.UserRequestUUID       // user-request domain
}

type QuestionOption_Type uint16

const (
	QuestionOption_Type_Unset   QuestionOption_Type = 0
	QuestionOption_Type_Correct QuestionOption_Type = (1 << iota)

	QuestionOption_Type_Limit // QuestionOptionMultipleChoice

	// Without need to be an option to prevent impact on overall result
	QuestionOption_Type_Neutral

	QuestionOption_Type_ForceToFillOther
	QuestionOption_Type_ForceToContinueInOther
	QuestionOption_Type_Question
	QuestionOption_Type_Questionnaire

	QuestionOption_Type_DropList
)
