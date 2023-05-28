/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionRating indicate the domain record data fields.
type QuestionRating interface {
	QuestionID() QuestionUUID       //
	Type() QuestionRating_Type      //
	Max() uint8                     //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type QuestionRating_StorageServices interface {
	Save(f QuestionRating) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (f QuestionRating, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByType(t QuestionRating_Type, offset, limit uint64) (questionIDs []QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type QuestionRating_Type uint16

const (
	QuestionRating_Type_Unset             QuestionRating_Type = 0
	QuestionRating_Type_LikertScale_Emoji QuestionRating_Type = (1 << iota)
	QuestionRating_Type_LikertScale_Color
	QuestionRating_Type_LikertScale_Range // bipolar scale
	QuestionRating_Type_Star
	QuestionRating_Type_Number
	QuestionRating_Type_Text
	QuestionRating_Type_Label

	QuestionRating_Type_ForceToFill
	QuestionRating_Type_ForceToContinue
)
