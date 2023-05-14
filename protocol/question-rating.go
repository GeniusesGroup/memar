/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TODO::: Can be rating as stand-alone domain??

// QuestionRating indicate the domain record data fields.
type QuestionRating interface {
	QuestionID() QuestionUUID       //
	Type() QuestionRating_Type      //
	Max() uint8                     //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID // user-request domain
}

type QuestionRating_Type uint8

const (
	QuestionRating_Type_Unset QuestionRating_Type = iota
	QuestionRating_Type_Star
	QuestionRating_Type_Number
	QuestionRating_Type_Text
	QuestionRating_Type_Label

	// QuestionOption_Type_ForceToFillOther
)
