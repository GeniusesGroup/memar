/* For license and copyright information please see the LEGAL file in the code repository */

package qop

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionOptionID() QuestionOptionUUID //
	Type() Type                           //
	Significance_Positive() uint64        //
	Significance_Negative() uint64        //
	SaveTime() protocol.Time              //
	RequestID() urp.UserRequestUUID       //
}

type Type uint16

const (
	Type_Unset   Type = 0
	Type_Correct Type = (1 << iota)

	Type_Limit // QuestionOptionMultipleChoice

	// Without need to be an option to prevent impact on overall result
	Type_Neutral

	Type_ForceToFill_Question
	Type_ForceToFill_Questionnaire
	Type_ForceToContinue_Question
	Type_ForceToContinue_Questionnaire

	// It will effect on other option analytical.
	Type_Criterion
)
