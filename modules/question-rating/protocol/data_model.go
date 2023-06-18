/* For license and copyright information please see the LEGAL file in the code repository */

package qrp

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID    //
	Type() Type                     //
	Max() uint8                     //
	SaveTime() protocol.Time        // Save time
	RequestID() urp.UserRequestUUID //
}

type Type uint16

const (
	Type_Unset             Type = 0
	Type_LikertScale_Emoji Type = (1 << iota)
	Type_LikertScale_Color
	Type_LikertScale_Range // bipolar scale
	Type_Star
	Type_Number
	Type_Text
	Type_Label

	Type_ForceToFill
	Type_ForceToContinue
)
